#!/usr/bin/env python3
"""Maintain a single-PM Markdown task register; messages are data, never shell code."""
import argparse
from copy import deepcopy
import json
import os
from pathlib import Path
import re
import sys
import tempfile

sys.dont_write_bytecode = True
from context import read_json
from task_gate import canonical_bytes, digest, evaluate, identity, require, TASK_KEYS, DELIVERY_KEYS, REVIEW_KEYS

FENCE = re.compile(r"```qore-task\n(.*?)\n```", re.S)


def load_register(path):
    text = path.read_text(encoding="utf-8")
    blocks = FENCE.findall(text)
    require(len(blocks) == 1, "expected exactly one qore-task JSON block per register file")
    register = json.loads(blocks[0])
    require(register.get("schema") == "qore-task/1", "unknown task register")
    return text, register


def save_register(path, text, register):
    """Atomically save the whole Markdown document under the one-active-PM convention."""
    block = "```qore-task\n" + json.dumps(register, indent=2, ensure_ascii=False, allow_nan=False) + "\n```"
    updated = FENCE.sub(lambda _: block, text, count=1)
    require(updated != text or FENCE.search(text), "missing task block")
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as handle:
            temporary = handle.name
            handle.write(updated.encode("utf-8")); handle.flush(); os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary and Path(temporary).exists():
            Path(temporary).unlink()


def initialize(snapshot, assignment_message_id, dependencies_satisfied=False, authorization_satisfied=False):
    require(type(snapshot.get("task_revision")) is int and snapshot["task_revision"] >= 1, "invalid task revision")
    for key in ("task_id", "objective", "authorized_scope", "criteria", "required_check_ids", "expected_results"):
        require(bool(snapshot.get(key)), "missing criteria field: " + key)
    require(set(snapshot["required_check_ids"]) == set(snapshot["expected_results"]), "incomplete required check inventory")
    return {"schema": "qore-task/1", **identity(snapshot, TASK_KEYS[:2]),
            "criteria_sha256": digest(canonical_bytes(snapshot)), "objective": snapshot["objective"],
            "state": "ASSIGNED", "awaiting": "production_ack", "next_action_owner": "production",
            "assignment_message_id": str(assignment_message_id), "dependencies_satisfied": dependencies_satisfied,
            "authorization_satisfied": authorization_satisfied, "processed_message_ids": [], "decisions": [],
            "accepted_identity": None, "cursor": None}


def consume(register, messages):
    """Reconcile a complete fetched window, including read messages, without transport ACKs.

    A fetch timeout supplies no messages and leaves state/awaiting unchanged.
    This function never sends assignments, creates a reviewer, or reruns production.
    """
    result = deepcopy(register)
    for message in messages:
        message_id = str(message["id"])
        if message_id in result["processed_message_ids"]:
            continue
        body = message.get("body", {})
        reason, action = "stale or unrecognized message", "REJECT"
        try:
            current = identity(result, TASK_KEYS)
            require(identity(body, TASK_KEYS) == current, "stale task criteria")
            if body.get("kind") == "production_ack":
                require(result["state"] == "ASSIGNED" and result["awaiting"] == "production_ack", "not awaiting task acceptance")
                require(str(body["assignment_message_id"]) == result["assignment_message_id"], "wrong assignment")
                result.update(state="IN_PROGRESS", awaiting="delivery", next_action_owner="production")
                action, reason = "ACCEPT_ACK", "explicit production task acceptance"
            elif body.get("kind") == "delivery":
                require(result["state"] == "IN_PROGRESS" and result["awaiting"] == "delivery", "not awaiting delivery")
                delivery = {**body, "delivery_message_id": message_id}
                identity(delivery, DELIVERY_KEYS)
                result.update(**identity(delivery, DELIVERY_KEYS), artifact_path=body["artifact_path"],
                              artifact_kind=body.get("artifact_kind", "file"), delivery=delivery,
                              state="REVIEW_REQUIRED", awaiting=None, next_action_owner="pm")
                action, reason = "RECEIVE_DELIVERY", "delivery recorded; independent review still required"
            elif body.get("kind") == "review_verdict":
                require(result["state"] == "REVIEW_REQUIRED" and result["awaiting"] == "review_verdict", "not awaiting review")
                require(identity(body, REVIEW_KEYS) == identity(result, REVIEW_KEYS), "stale review request or artifact")
                result["pending_verdict"] = {**body, "message_id": message_id}
                result["next_action_owner"] = "pm"
                action, reason = "RECEIVE_VERDICT", "completion gate still required"
                if body.get("verdict") == "FAIL":
                    result.update(state="CHANGES_REQUIRED", awaiting=None, next_action_owner="production")
                elif body.get("verdict") in ("PARTIAL", "BLOCKED"):
                    result.update(state="BLOCKED", awaiting=None, next_action_owner="pm")
        except (ValueError, KeyError, TypeError) as error:
            reason = str(error)
        result["processed_message_ids"].append(message_id)
        result["decisions"].append({"message_id": message_id, "action": action, "reason": reason})
        # Retain an overlap timestamp, not unread state. The receive caller refetches inclusively.
        if message.get("created_ts"):
            result["cursor"] = message["created_ts"]
    return result


def request_review(register, request):
    require(register["state"] == "REVIEW_REQUIRED" and register["awaiting"] is None, "not ready for a fresh review request")
    require(identity(request, DELIVERY_KEYS) == identity(register, DELIVERY_KEYS), "review request targets old delivery")
    require(bool(request["review_request_id"]) and bool(request["review_session_id"]) and bool(request["review_run_id"]), "missing review identity")
    require(request.get("review_session_fresh") is True, "reviewer must be designated fresh")
    result = deepcopy(register)
    result.update(**{key: request[key] for key in ("review_request_id", "review_session_id", "review_run_id", "review_session_fresh")},
                  request=request, awaiting="review_verdict", next_action_owner="reviewer")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("init"); p.add_argument("--criteria", type=Path, required=True); p.add_argument("--register", type=Path, required=True); p.add_argument("--assignment-id", required=True)
    p.add_argument("--dependencies-satisfied", action="store_true"); p.add_argument("--authorization-satisfied", action="store_true")
    for command in ("consume", "request-review", "complete", "show"):
        p = sub.add_parser(command); p.add_argument("--register", type=Path, required=True)
        if command in ("consume", "request-review"): p.add_argument("--input", type=Path, required=True)
        if command == "complete": p.add_argument("--criteria", type=Path, required=True); p.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == "init":
            require(not args.register.exists(), "register exists; preserve it")
            register = initialize(read_json(args.criteria), args.assignment_id, args.dependencies_satisfied, args.authorization_satisfied)
            args.register.parent.mkdir(parents=True, exist_ok=True)
            text = "# Private task register\n\nOne active PM writer. Transport ACK is not task acceptance.\n\n```qore-task\n{}\n```\n"
        else:
            text, register = load_register(args.register)
            if args.command == "consume": register = consume(register, read_json(args.input))
            elif args.command == "request-review": register = request_review(register, read_json(args.input))
            elif args.command == "complete":
                verdict = register["pending_verdict"]
                # Received is not accepted: only the gate may add this verdict to completion IDs.
                candidate = deepcopy(register)
                if candidate["state"] != "DONE":
                    candidate["processed_message_ids"] = [key for key in candidate["processed_message_ids"] if key != verdict["message_id"]]
                decision, register = evaluate(candidate, read_json(args.criteria), candidate["delivery"], candidate["request"], verdict, args.root)
                if decision["action"] != "NOOP": register["decisions"].append(decision)
        if args.command != "show": save_register(args.register, text, register)
        print(json.dumps(register, indent=2))
        return 0
    except (ValueError, KeyError, TypeError, OSError) as error:
        print(json.dumps({"valid": False, "error": str(error)}), file=sys.stderr); return 1


if __name__ == "__main__":
    raise SystemExit(main())
