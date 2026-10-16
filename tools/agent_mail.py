#!/usr/bin/env python3
"""Optional loopback Agent Mail receive adapter with durable decision-before-ACK ordering."""
import argparse
import json
import os
from pathlib import Path
import sys
import time
from urllib.parse import urlsplit
import urllib.request

sys.dont_write_bytecode = True
from coordination import load_register, save_register, consume
from task_gate import require


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, request, *_):
        raise ValueError("Agent Mail endpoint redirects are refused")


class Client:
    def __init__(self, url, token, timeout=30):
        parsed = urlsplit(url)
        require(parsed.scheme == "http" and parsed.hostname in ("127.0.0.1", "::1", "localhost")
                and not parsed.username and not parsed.password, "only an explicit loopback HTTP endpoint is supported")
        require(bool(token), "QORE_AGENT_MAIL_TOKEN is unavailable")
        self.url, self.token, self.timeout, self.counter = url, token, timeout, 0

    def call(self, name, arguments):
        self.counter += 1
        request = urllib.request.Request(self.url, data=json.dumps({"jsonrpc": "2.0", "id": self.counter,
            "method": "tools/call", "params": {"name": name, "arguments": arguments}}).encode(),
            headers={"Authorization": "Bearer " + self.token, "Content-Type": "application/json", "Accept": "application/json, text/event-stream"})
        with urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect).open(request, timeout=self.timeout) as response:
            raw = response.read().decode()
        if raw.startswith(("event:", "data:")):
            raw = "\n".join(line[6:] for line in raw.splitlines() if line.startswith("data: "))
        packet = json.loads(raw)
        require("error" not in packet, "Agent Mail RPC failed")
        result = packet["result"]
        require(not result.get("isError"), "Agent Mail tool failed")
        content = result.get("structuredContent")
        if content is None:
            texts = [block["text"] for block in result.get("content", []) if block.get("type") == "text"]
            require(len(texts) == 1, "expected one structured Agent Mail response")
            content = json.loads(texts[0])
        return content


def receive(client, register_path, project, agent, thread, seconds=120):
    require(0 <= seconds <= 120, "receive window must be between 0 and 120 seconds")
    # Zero means one snapshot, still with a finite 30-second scheduling budget.
    deadline = time.monotonic() + (seconds or 30)
    attempts, acknowledgements, reads = 0, [], 0
    while True:
        text, current = load_register(register_path)
        if time.monotonic() >= deadline:
            return {"status": "WAITING", "state": current["state"], "awaiting": current["awaiting"], "reads": reads,
                    "resume": "Operator resumes another bounded receive turn; no assignment is resent."}
        try:
            if isinstance(client, Client):
                client.timeout = max(0.001, min(30, deadline - time.monotonic()))
            # Include read messages. Fetch the complete bounded trial inbox rather than losing
            # out-of-order/late messages at a timestamp cursor. Refuse a full page: no false completeness.
            packet = client.call("fetch_inbox", {"project_key": project, "agent_name": agent, "include_bodies": True,
                                                  "unread_only": False, "limit": 1000})
            entries = packet if isinstance(packet, list) else packet.get("messages", [])
            require(len(entries) < 1000, "inbox page is full; narrow/archive the project before resuming")
            normalized = []
            for entry in sorted(entries, key=lambda item: int(item["id"])):
                if entry.get("thread_id") != thread:
                    continue
                try:
                    body = json.loads(entry.get("body_md", "{}"))
                except ValueError:
                    body = {}
                if not isinstance(body, dict): body = {}
                normalized.append({"id": entry["id"], "body": body, "created_ts": entry.get("created_ts")})
            resumed = dict(current)
            if current.get("state") == "BLOCKED" and current.get("blocked_from_state"):
                resumed["state"] = resumed.pop("blocked_from_state")
                resumed["next_action_owner"] = resumed.pop("blocked_next_action_owner", current.get("next_action_owner"))
                resumed.pop("resume_action", None)
            updated = consume(resumed, normalized); reads += 1
            # Durable state, decision and IDs precede EVERY transport acknowledgement.
            save_register(register_path, text, updated)
            for entry in entries:
                if entry.get("thread_id") == thread and str(entry["id"]) in updated["processed_message_ids"] and entry.get("ack_required"):
                    remaining = deadline - time.monotonic()
                    if remaining <= 0:
                        return {"status": "RECEIVED" if updated["processed_message_ids"] != current["processed_message_ids"] else "WAITING",
                                "reads": reads, "state": updated["state"], "awaiting": updated["awaiting"],
                                "acknowledged": acknowledgements, "resume": "Receive again to acknowledge remaining durable decisions."}
                    if isinstance(client, Client): client.timeout = min(30, remaining)
                    client.call("acknowledge_message", {"project_key": project, "agent_name": agent, "message_id": entry["id"]})
                    acknowledgements.append(entry["id"])
            if updated["processed_message_ids"] != current["processed_message_ids"]:
                return {"status": "RECEIVED", "reads": reads, "state": updated["state"], "awaiting": updated["awaiting"], "acknowledged": acknowledgements}
            current = updated
            attempts = 0
        except (OSError, ValueError, KeyError, TypeError) as error:
            attempts += 1
            if attempts >= 2:
                text, current = load_register(register_path)
                if current["state"] != "BLOCKED":
                    current["blocked_from_state"] = current["state"]
                    current["blocked_next_action_owner"] = current["next_action_owner"]
                current.update(state="BLOCKED", next_action_owner="pm", resume_action="Reconcile this task inbox using the existing assignment; do not resend or start another reviewer.")
                current["decisions"].append({"action": "RECEIVE_BLOCKED", "reason": type(error).__name__})
                save_register(register_path, text, current)
                return {"status": "BLOCKED", "reason": type(error).__name__, "reads": reads}
        remaining = deadline - time.monotonic()
        if seconds == 0 or remaining <= 0:
            return {"status": "WAITING", "state": current["state"], "awaiting": current["awaiting"], "reads": reads,
                    "resume": "Operator resumes another bounded receive turn; no assignment is resent."}
        time.sleep(min(2, remaining))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", required=True); parser.add_argument("--project", required=True); parser.add_argument("--agent", required=True)
    parser.add_argument("--thread", required=True); parser.add_argument("--register", type=Path, required=True)
    parser.add_argument("--seconds", type=int, default=120)
    args = parser.parse_args()
    try:
        result = receive(Client(args.url, os.environ.get("QORE_AGENT_MAIL_TOKEN")), args.register, args.project, args.agent, args.thread, args.seconds)
        print(json.dumps(result, indent=2)); return 1 if result["status"] == "BLOCKED" else 0
    except (ValueError, OSError, TypeError, KeyError) as error:
        print(json.dumps({"status": "BLOCKED", "reason": type(error).__name__}), file=sys.stderr); return 1


if __name__ == "__main__":
    raise SystemExit(main())
