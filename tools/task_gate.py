"""Check cooperative task completion against current criteria and actual proof bytes."""
from copy import deepcopy
from hashlib import sha256
import json
import os
from pathlib import Path
import tempfile

TASK_KEYS = ("task_id", "task_revision", "criteria_sha256")
DELIVERY_KEYS = TASK_KEYS + ("artifact_revision", "artifact_sha256", "delivery_message_id")
REVIEW_KEYS = DELIVERY_KEYS + ("review_request_id",)


class Rejected(ValueError):
    pass


def canonical_bytes(value):
    """Canonical criteria bytes, including the final LF and rejection of NaN."""
    return (json.dumps(value, sort_keys=True, ensure_ascii=False,
                       separators=(",", ":"), allow_nan=False) + "\n").encode("utf-8")


def digest(data):
    return sha256(data).hexdigest()


def identity(obj, keys):
    try:
        selected = {key: obj[key] for key in keys}
    except KeyError as error:
        raise Rejected("missing identity: " + str(error)) from error
    if any(value is None or value == "" for value in selected.values()):
        raise Rejected("empty identity")
    return selected


def require(condition, reason):
    if not condition:
        raise Rejected(reason)


def contained_bytes(root, relative):
    require(isinstance(relative, str) and relative and not Path(relative).is_absolute()
            and ".." not in Path(relative).parts and "\\" not in relative,
            "expected a contained relative path")
    root = Path(root).resolve()
    path = (root / relative).resolve()
    require(path.is_relative_to(root), "path escapes proof root")
    require(path.is_file(), "referenced bytes unavailable")
    return path.read_bytes()


def artifact_bytes(root, register):
    raw = contained_bytes(root, register["artifact_path"])
    if register.get("artifact_kind", "file") == "manifest":
        manifest = json.loads(raw)
        require(isinstance(manifest, dict) and manifest.get("schema") == "qore-task-files/1",
                "unknown artifact manifest")
        files = manifest.get("files")
        require(isinstance(files, list) and bool(files), "empty artifact manifest")
        names = [item["path"] for item in files]
        require(names == sorted(set(names)), "manifest must have sorted unique paths")
        for item in files:
            require(digest(contained_bytes(root, item["path"])) == item.get("sha256"),
                    "actual manifest file bytes differ: " + item["path"])
    else:
        require(register.get("artifact_kind", "file") == "file", "unknown artifact kind")
    return raw


def evaluate(register, snapshot, delivery, request, verdict, root):
    """Return (decision, replacement register); rejected input never mutates state.

    Supports one file or a contained sorted file manifest. Caller supplies trusted cooperative
    registry, dependency and authorization decisions; these are not inferred
    from received message text. Proof content is checked for consistency, not
    independently established truth or actor authentication.
    """
    current = identity(register, REVIEW_KEYS)
    require(type(snapshot.get("task_revision")) is int, "revision must be integer")
    require(snapshot["task_revision"] >= 1, "revision must be positive")
    require(identity(snapshot, TASK_KEYS[:2]) == identity(current, TASK_KEYS[:2]),
            "snapshot task or revision differs")
    require(digest(canonical_bytes(snapshot)) == current["criteria_sha256"],
            "current criteria bytes changed")
    for key in ("objective", "authorized_scope", "criteria", "required_check_ids", "expected_results"):
        require(key in snapshot, "incomplete criteria snapshot: " + key)
    checks = snapshot["required_check_ids"]
    require(isinstance(checks, list) and bool(checks), "required checks must be nonempty")
    require(all(isinstance(check, str) and check for check in checks), "invalid check IDs")
    require(len(checks) == len(set(checks)), "duplicate required check")
    require(set(snapshot["expected_results"]) == set(checks), "expected check results differ")
    require(register.get("dependencies_satisfied") is True, "dependencies unsatisfied")
    require(register.get("authorization_satisfied") is True, "authorization unsatisfied")
    require(identity(delivery, DELIVERY_KEYS) == identity(current, DELIVERY_KEYS), "delivery identity differs")
    for envelope in (request, verdict):
        require(identity(envelope, REVIEW_KEYS) == current, "review identity differs")
    require(delivery.get("artifact_path") == register.get("artifact_path"), "artifact reference differs")
    artifact = artifact_bytes(root, register)
    require(digest(artifact) == current["artifact_sha256"], "actual artifact bytes differ")
    for envelope in (request, verdict):
        require(envelope.get("review_session_id") == register["review_session_id"], "review session differs")
        require(envelope.get("review_run_id") == register["review_run_id"], "review run differs")
    require(register.get("review_session_fresh") is True, "review session not designated fresh")
    require(verdict.get("verdict") == "PASS", "verdict is not PASS")
    require(isinstance(verdict.get("message_id"), str) and bool(verdict["message_id"]), "missing verdict message ID")
    proofs = verdict.get("proofs", [])
    require(len(proofs) == len(checks), "required proof missing or duplicated")
    require({proof.get("check_id") for proof in proofs} == set(checks), "proof check IDs differ")
    for proof in proofs:
        raw = contained_bytes(root, proof["path"])
        require(digest(raw) == proof.get("sha256"), "actual evidence bytes differ")
        record = json.loads(raw)
        require(identity(record, REVIEW_KEYS) == current, "proof identity differs")
        require(record.get("review_session_id") == register["review_session_id"], "proof session differs")
        require(record.get("review_run_id") == register["review_run_id"], "proof run differs")
        check_id = proof["check_id"]
        require(record.get("check_id") == check_id, "proof check differs")
        require(record.get("result") == snapshot["expected_results"][check_id], "proof result differs")
        require(record.get("result") not in ("PARTIAL", "BLOCKED"), "incomplete check result")
    acceptance = dict(current, review_session_id=register["review_session_id"],
                      review_run_id=register["review_run_id"], verdict_message_id=verdict["message_id"])
    if register.get("state") == "DONE":
        require(register.get("accepted_identity") == acceptance, "different acceptance after DONE")
        return {"action": "NOOP", "reason": "already consumed", "acceptance": acceptance}, deepcopy(register)
    require(register.get("state") == "REVIEW_REQUIRED" and register.get("awaiting") == "review_verdict",
            "task does not await current review")
    require(register.get("accepted_identity") is None, "acceptance already consumed")
    require(verdict["message_id"] not in register.get("processed_message_ids", []), "verdict already processed")
    replacement = deepcopy(register)
    replacement.update(state="DONE", awaiting=None, next_action_owner=None,
                       accepted_identity=acceptance, accepted_proofs=deepcopy(proofs))
    replacement["processed_message_ids"] = list(dict.fromkeys(
        register.get("processed_message_ids", []) + [delivery["delivery_message_id"],
        request["review_request_id"], verdict["message_id"]]))
    return {"action": "DONE", "reason": "current identity and required proof bytes verified", "acceptance": acceptance}, replacement


def atomic_write(path, replacement):
    """Single PM writer only; no locking, transport ACK, or concurrent writer support."""
    path = Path(path)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as handle:
            temporary = handle.name
            handle.write(canonical_bytes(replacement))
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary and Path(temporary).exists():
            Path(temporary).unlink()
