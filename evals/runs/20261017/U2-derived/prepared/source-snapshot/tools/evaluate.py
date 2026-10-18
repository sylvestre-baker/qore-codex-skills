#!/usr/bin/env python3
"""Prepare isolated task inputs and validate recorded observations; never run a model."""
import argparse
from datetime import datetime
import hashlib
import json
import math
from pathlib import Path
import re
import shutil
import sys
import tempfile

sys.dont_write_bytecode = True
from context import contained as resolved_contained, digest, read_json
import qore
from run_contract import validate_run as validate_qore_run

ROOT = Path(__file__).resolve().parents[1]
CONDITIONS = ("baseline", "generic", "derived")
METHOD_SKILLS = {"plan": "qore-plan", "review": "qore-review", "ux": "qore-ux-review"}
HEX = re.compile(r"[a-f0-9]{64}")


def contained(root, relative, *, must_exist=True):
    """Reject aliases within an evidence boundary before resolved containment."""
    result = resolved_contained(root, relative, must_exist=must_exist)
    base = Path(root)
    if base.is_symlink():
        raise ValueError("Symlinked boundary root")
    current = base
    for part in Path(relative).parts:
        current /= part
        if current.is_symlink():
            raise ValueError("Symlinked resource or ancestor: " + relative)
    return result


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def identity(value):
    return hashlib.sha256(encoded(value)).hexdigest()


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def instant(value):
    if not isinstance(value, str):
        raise ValueError("A timestamp must be a timezone-aware ISO string")
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("A timestamp needs a timezone")
    return parsed


def text(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Missing nonempty string: " + label)
    return value


def sha(value, label):
    if not isinstance(value, str) or not HEX.fullmatch(value):
        raise ValueError("Invalid SHA-256: " + label)
    return value


def inventory(folder):
    if folder.is_symlink():
        raise ValueError("Symlinked inventory root")
    return [{"path": p.relative_to(folder).as_posix(), "sha256": digest(p)} for p in qore.files_under(folder)]


def configuration(source_root=None):
    source_root = source_root or ROOT
    path = source_root / "evals/scenarios.json"
    data = read_json(path)
    if not isinstance(data, dict) or data.get("schema") != "qore-eval-scenarios/1":
        raise ValueError("Expected qore-eval-scenarios/1")
    scenarios = data.get("scenarios")
    if not isinstance(scenarios, list) or len(scenarios) != 6:
        raise ValueError("Exactly six declared scenarios are required")
    by_id = {}
    for scenario in scenarios:
        sid = text(scenario.get("id"), "scenario id")
        if sid in by_id or scenario.get("method") not in METHOD_SKILLS:
            raise ValueError("Duplicate scenario or unknown method: " + sid)
        text(scenario.get("prompt"), "scenario prompt")
        criteria = scenario.get("criteria")
        if not isinstance(criteria, list) or not criteria or len(criteria) != len(set(criteria)) or set(criteria) - set(data.get("criteria", {})):
            raise ValueError("Unknown or duplicate scenario criteria")
        if scenario.get("target") is not None:
            contained(source_root, scenario["target"])
        by_id[sid] = scenario
    expected = {(s, c) for s in by_id for c in CONDITIONS}
    order = data.get("order")
    if not isinstance(order, list) or len(order) != 18 or any(not isinstance(p, list) or len(p) != 2 for p in order) or {tuple(p) for p in order} != expected:
        raise ValueError("The order must contain every scenario/condition exactly once")
    return data, by_id, digest(path)


def materialize_worker(source_root, config, scenario, condition, worker):
    """Rebuild the entire allowed worker closure without executing snapshot code."""
    project = contained_directory(source_root, config["project_root"])
    worker.mkdir()
    for relative in config["common_sources"]:
        target = worker / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(contained(project, relative), target)
    if scenario.get("target"):
        target = worker / "target/verification-protocol.md"
        target.parent.mkdir()
        shutil.copyfile(contained(source_root, scenario["target"]), target)
    skill_name = None
    if condition != "baseline":
        base = METHOD_SKILLS[scenario["method"]]
        if condition == "derived":
            with tempfile.TemporaryDirectory(prefix="qore-eval-derive-") as temporary:
                derived = Path(temporary) / "skills"
                previous_root = qore.ROOT
                try:
                    qore.ROOT = source_root
                    profile_path = contained(source_root, config["profile"])
                    qore.derive(profile_path, project, derived)
                finally:
                    qore.ROOT = previous_root
                skill_name = base + "-" + read_json(profile_path)["id"]
                destination = worker / ".agents/skills" / skill_name
                destination.parent.mkdir(parents=True)
                shutil.copytree(derived / skill_name, destination)
        else:
            skill_name = base
            source = contained_directory(source_root, "skills/" + base)
            qore.check_references(source)
            destination = worker / ".agents/skills" / skill_name
            destination.parent.mkdir(parents=True)
            shutil.copytree(source, destination)
            qore.make_skill_manifest(destination)
    prompt = ("Use $" + skill_name + ".\n\n" if skill_name else "") + scenario["prompt"]
    prompt += ("\n\nRead the original project sources: surface-contract.json, checks/check_contract.py and observation-policy.json. "
               "The supplied tutorial protocol, if present, is a task target rather than project authority. "
               "Write outputs outside the input folder. Do not alter supplied input or skill resources. "
               "Use only this cell's supplied resources and feedback, never previous reports or network answer retrieval.\n")
    if scenario["method"] == "ux":
        prompt += ("\nBrowser execution is operator-mediated equally in every condition. Submit a complete supported JSON action array "
                   "of at most 40 actions, starting from entry. Each observation uses a fresh context and begins with the probe's "
                   "automatic Tab capability check. At most six requests are permitted. The operator returns actual captures, DOM, "
                   "events and diagnostics without correcting actions or suggesting conclusions.\n")
    (worker / "TASK.md").write_text(prompt, encoding="utf-8")
    return skill_name


def candidate():
    """Bind executable inputs without letting later results change candidate identity."""
    selected = list(qore.files_under(ROOT / "skills"))
    selected += list(qore.files_under(ROOT / "evals/fixtures"))
    selected += [ROOT / p for p in (
        "evals/scenarios.json", "profiles/qaizen-labs.json", "tools/evaluate.py",
        "tools/qore.py", "tools/context.py", "tools/run_contract.py", "tools/browser_probe.mjs",
        "tools/clean_room.sh", "schemas/qore-eval-run.schema.json",
    )]
    selected += list(qore.files_under(ROOT / "examples/qaizen-labs/checks"))
    selected += [ROOT / "examples/qaizen-labs" / name for name in ("surface-contract.json", "observation-policy.json")]
    resources = [{"path": p.relative_to(ROOT).as_posix(), "sha256": digest(p)} for p in sorted(set(selected))]
    return {"schema": "qore-eval-candidate/1", "resources": resources, "sha256": identity(resources)}


def prepare(scenario_id, condition, output):
    config, scenarios, config_sha = configuration()
    if scenario_id not in scenarios or condition not in CONDITIONS:
        raise ValueError("Unknown scenario or condition")
    if output.exists() or output.is_symlink():
        raise ValueError("Output exists; choose a new staging destination")
    scenario = scenarios[scenario_id]
    candidate_info = candidate()
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix=".qore-eval-", dir=output.parent))
    try:
        worker = temporary / "worker"
        skill_name = materialize_worker(ROOT, config, scenario, condition, worker)
        resources = inventory(worker)
        skill_resources = [r for r in resources if r["path"].startswith(".agents/")]
        manifest = {"schema": "qore-eval-inputs/1", "scenario_id": scenario_id, "condition": condition,
                    "method": scenario["method"], "scenarios_sha256": config_sha,
                    "candidate_sha256": candidate_info["sha256"], "condition_resources_sha256": identity(skill_resources),
                    "resources": resources, "limit": "Stage only worker/, not this preparation directory or the author repository."}
        write(temporary / "input-manifest.json", manifest)
        if candidate()["sha256"] != candidate_info["sha256"]:
            raise ValueError("Candidate changed during preparation; use a frozen snapshot")
        write(temporary / "candidate.json", candidate_info)
        for item in candidate_info["resources"]:
            source = contained(ROOT, item["path"])
            target = temporary / "source-snapshot" / item["path"]
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
            if digest(target) != item["sha256"]:
                raise ValueError("Source changed while copying frozen candidate")
        write(temporary / "instructions.json", {"status": "PREPARED_NOT_EXECUTED", "skill": skill_name,
              "budgets": config["budgets"], "criteria": scenario["criteria"],
              "required_preflight": ["Enforced input and command-network isolation, including every child context",
                                     "Actual model authentication and method roles", "Pre/post input integrity",
                                     "Qualified activation guard and neutral browser relay for UX"],
              "limit": "Preparation and structural checks do not establish isolation, execution or comparative quality."})
        temporary.rename(output)
    finally:
        if temporary.exists():
            shutil.rmtree(temporary)
    return {"status": "PREPARED_NOT_EXECUTED", "output": str(output), "input_manifest_sha256": digest(output / "input-manifest.json"),
            "candidate_sha256": manifest["candidate_sha256"], "files": len(resources), "model_called": False}


def contained_directory(root, relative):
    path = contained(root, relative, must_exist=False)
    if not path.is_dir() or path.is_symlink():
        raise ValueError("Required directory is absent or symlinked: " + relative)
    return path


def check_inputs(manifest_path):
    manifest = read_json(manifest_path)
    if not isinstance(manifest, dict) or manifest.get("schema") != "qore-eval-inputs/1":
        raise ValueError("Expected qore-eval-inputs/1")
    worker = manifest_path.parent / "worker"
    records = manifest.get("resources")
    if not isinstance(records, list) or not records:
        raise ValueError("Input manifest needs explicit resources")
    seen, changed = set(), []
    for record in records:
        name = record.get("path")
        if name in seen:
            raise ValueError("Duplicate input resource")
        seen.add(name)
        path = contained(worker, name, must_exist=False)
        sha(record.get("sha256"), "input resource")
        if path.is_symlink():
            raise ValueError("Symlinked input resource: " + name)
        if not path.is_file() or digest(path) != record["sha256"]:
            changed.append(name)
    actual = {p["path"] for p in inventory(worker)}
    changed += sorted(actual - seen)
    return manifest, sorted(set(changed))


def check_record(record_path, evidence_root):
    config, scenarios, config_sha = configuration()
    run = read_json(record_path)
    if not isinstance(run, dict) or run.get("schema") != "qore-eval-run/1":
        raise ValueError("Expected qore-eval-run/1")
    for field in ("id", "series_id"):
        text(run.get(field), field)
    if type(run.get("trial")) is not int or run["trial"] < 1:
        raise ValueError("trial must be a positive integer")
    sid, condition = run.get("scenario_id"), run.get("condition")
    if sid not in scenarios or condition not in CONDITIONS:
        raise ValueError("Unknown scenario or condition")
    for field in ("candidate_sha256", "input_manifest_sha256", "condition_resources_sha256"):
        sha(run.get(field), field)
    manifest_path = contained(evidence_root, run.get("input_manifest"))
    if digest(manifest_path) != run["input_manifest_sha256"]:
        raise ValueError("Input manifest digest mismatch")
    manifest, changed = check_inputs(manifest_path)
    source_candidate = read_json(contained(manifest_path.parent, "candidate.json"))
    if not isinstance(source_candidate, dict) or source_candidate.get("schema") != "qore-eval-candidate/1" or identity(source_candidate.get("resources")) != run["candidate_sha256"] or source_candidate.get("sha256") != run["candidate_sha256"]:
        raise ValueError("Candidate resource manifest mismatch")
    snapshot = contained_directory(manifest_path.parent, "source-snapshot")
    frozen_resources = source_candidate["resources"]
    if inventory(snapshot) != frozen_resources:
        raise ValueError("Frozen candidate source snapshot differs from its inventory")
    config, scenarios, config_sha = configuration(snapshot)
    if sid not in scenarios:
        raise ValueError("Scenario is absent from its frozen definition")
    with tempfile.TemporaryDirectory(prefix="qore-eval-expected-") as directory:
        expected_worker = Path(directory) / "worker"
        materialize_worker(snapshot, config, scenarios[sid], condition, expected_worker)
        if inventory(expected_worker) != manifest["resources"]:
            raise ValueError("Frozen worker resource closure or task instructions mismatch")
    original = {r["path"]: r["sha256"] for r in source_candidate["resources"]}
    supplied = {r["path"]: r["sha256"] for r in manifest["resources"]}
    for name in config["common_sources"]:
        if supplied.get(name) != original.get(config["project_root"] + "/" + name):
            raise ValueError("Authoritative source differs from the candidate: " + name)
    scenario_target = scenarios[sid].get("target")
    if scenario_target and supplied.get("target/verification-protocol.md") != original.get(scenario_target):
        raise ValueError("Task target differs from the frozen scenario")
    for field in ("scenario_id", "condition", "candidate_sha256", "condition_resources_sha256"):
        if manifest.get(field) != run[field]:
            raise ValueError("Input identity mismatch: " + field)
    if manifest.get("scenarios_sha256") != config_sha:
        raise ValueError("Scenario revision does not match current frozen definitions")
    actual_skill = [r for r in manifest["resources"] if r["path"].startswith(".agents/")]
    if identity(actual_skill) != run["condition_resources_sha256"]:
        raise ValueError("Condition resource digest mismatch")
    if (condition == "baseline") != (not actual_skill):
        raise ValueError("Skill resources do not match the declared condition")
    environment, resources = run.get("environment"), run.get("resources")
    if not isinstance(environment, dict) or not isinstance(resources, dict):
        raise ValueError("Environment and resources must be explicit objects")
    for field in ("operator", "host", "model", "actor_id"):
        text(environment.get(field), "environment." + field)
    if not isinstance(environment.get("tools"), dict) or not isinstance(environment.get("settings"), dict):
        raise ValueError("Tool versions and model settings must be explicit")
    start, end = instant(resources.get("started_at")), instant(resources.get("ended_at"))
    if end < start:
        raise ValueError("Execution ends before it starts")
    if resources.get("caps") != config["budgets"]:
        raise ValueError("Resource envelope differs from the frozen protocol")
    if (end - start).total_seconds() > config["budgets"]["wall_seconds"] and not resources.get("overrun_reason"):
        raise ValueError("Wall-time overrun requires an explicit explanation")
    if not isinstance(resources.get("children"), list):
        raise ValueError("Child context accounting must be explicit")
    actors = []
    child_windows = {}
    total_child_seconds = 0
    for child in resources["children"]:
        actors.append(text(child.get("actor_id"), "child actor"))
        child_start, child_end = instant(child.get("started_at")), instant(child.get("ended_at"))
        if not start <= child_start <= child_end <= end:
            raise ValueError("Child context times lie outside the trial")
        child_windows[actors[-1]] = (child_start, child_end)
        total_child_seconds += (child_end - child_start).total_seconds()
    if len(actors) != len(set(actors)):
        raise ValueError("Repeated child context identity")
    for field in ("tokens", "aggregate_agent_seconds"):
        value = resources.get(field)
        if value is None:
            text(resources.get("unavailable", {}).get(field), "Unavailable usage reason: " + field)
        elif isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value < 0:
            raise ValueError("Invalid actual usage: " + field)
    if resources.get("aggregate_agent_seconds") is not None and resources["aggregate_agent_seconds"] < total_child_seconds:
        raise ValueError("Aggregate agent time omits measured child durations")
    if resources.get("aggregate_agent_seconds") is not None and resources["aggregate_agent_seconds"] > config["budgets"]["aggregate_agent_seconds"] and not resources.get("overrun_reason"):
        raise ValueError("Aggregate-time overrun requires an explicit explanation")
    if not isinstance(run.get("limitations"), list):
        raise ValueError("Limitations must be explicit")
    artifacts = run.get("artifacts")
    if not isinstance(artifacts, list):
        raise ValueError("Artifacts must be a list")
    by_path = {}
    for artifact in artifacts:
        name = artifact.get("path")
        if name in by_path:
            raise ValueError("Duplicate evidence resource")
        path = contained(evidence_root, name)
        if path.is_symlink() or digest(path) != artifact.get("sha256"):
            raise ValueError("Altered evidence resource: " + name)
        if artifact.get("kind") not in ("execution", "source", "presentation"):
            raise ValueError("Unknown artifact kind")
        if artifact["kind"] == "execution":
            observed = instant(artifact.get("observed_at"))
            if not start <= observed <= end:
                raise ValueError("Execution evidence is outside this trial")
            packet = read_json(path)
            if not isinstance(packet, dict) or packet.get("schema") != "qore-eval-evidence/1" or "payload" not in packet:
                raise ValueError("Execution evidence needs an identity-bound envelope")
            for field in ("id", "candidate_sha256", "input_manifest_sha256"):
                key = "run_id" if field == "id" else field
                if packet.get(key) != run[field]:
                    raise ValueError("Execution evidence belongs to another trial")
            if packet.get("observed_at") != artifact["observed_at"]:
                raise ValueError("Execution evidence timestamp mismatch")
        by_path[name] = artifact

    def references(values, *, nonempty=False, execution=False):
        if not isinstance(values, list) or len(values) != len(set(values)) or any(v not in by_path for v in values) or (nonempty and not values):
            raise ValueError("Missing, duplicate or undeclared evidence reference")
        if execution and not any(by_path[p]["kind"] == "execution" for p in values):
            raise ValueError("An actual execution artifact is required")

    result = run.get("execution", {})
    coverage = result.get("coverage")
    if coverage not in ("COMPLETE", "PARTIAL", "BLOCKED"):
        raise ValueError("Unknown execution coverage")
    references(result.get("evidence"), nonempty=coverage == "COMPLETE", execution=coverage == "COMPLETE")
    if coverage != "COMPLETE":
        text(result.get("reason"), "Incomplete execution reason")
    isolation = environment.get("isolation", {})
    if isolation.get("status") not in ("PASS", "BLOCKED", "UNVERIFIED"):
        raise ValueError("Explicit isolation status is required")
    references(isolation.get("evidence"), nonempty=isolation.get("status") == "PASS", execution=isolation.get("status") == "PASS")
    if isolation.get("status") != "PASS" and coverage == "COMPLETE":
        raise ValueError("Missing isolation prevents a complete controlled trial")
    if condition == "baseline":
        if run.get("qore_run") is not None:
            raise ValueError("Baseline must not invent Qore method phases")
    else:
        link = run.get("qore_run")
        if not isinstance(link, dict):
            raise ValueError("Qore condition requires its method execution record")
        qpath = contained(evidence_root, link.get("path"))
        if digest(qpath) != link.get("sha256"):
            raise ValueError("Qore execution record digest mismatch")
        qrun = read_json(qpath)
        checked = validate_qore_run(qrun, qpath.parent)
        if qrun["id"] != run["id"] or qrun["environment"]["host"] != environment["host"] or qrun["environment"]["operator"] != environment["operator"]:
            raise ValueError("Qore method execution belongs to another trial or environment")
        for phase in qrun["phases"]:
            actor = phase["actor_id"]
            if phase["status"] == "PASS" and actor != environment.get("actor_id") and actor not in child_windows:
                raise ValueError("Qore phase actor is absent from trial resource accounting")
        for artifact in qrun["artifacts"]:
            if artifact["kind"] == "execution" and not start <= instant(artifact["observed_at"]) <= end:
                raise ValueError("Qore phase evidence is outside the current trial")
        if qrun["candidate_sha256"] != run["candidate_sha256"] or qrun["method"] != scenarios[sid]["method"]:
            raise ValueError("Qore record candidate or method mismatch")
        if qrun["target"]["snapshot_sha256"] != run["input_manifest_sha256"]:
            raise ValueError("Qore record target does not match the prepared trial")
        entrypoints = [r["path"] for r in manifest["resources"] if r["path"].startswith(".agents/skills/") and r["path"].endswith("/SKILL.md")]
        if len(entrypoints) != 1 or qrun["skill"] != entrypoints[0].split("/")[2]:
            raise ValueError("Qore record skill differs from the supplied entrypoint")
        if coverage != checked["coverage"]:
            raise ValueError("Evaluation coverage differs from its Qore execution")
        if (condition == "derived") != (qrun.get("profile") is not None):
            raise ValueError("Qore profile does not match the condition")
        if condition == "derived":
            p = contained(manifest_path.parent / "worker", entrypoints[0].rsplit("/", 1)[0] + "/references/project.json")
            profile = read_json(p)
            if qrun["profile"] != {"id": profile["id"], "version": profile["version"], "sha256": digest(p)}:
                raise ValueError("Qore record profile differs from the supplied profile")
    assessments = run.get("assessment")
    if not isinstance(assessments, list):
        raise ValueError("Assessment must be an explicit list")
    if len(assessments) != len(scenarios[sid]["criteria"]) or {a.get("criterion") for a in assessments} != set(scenarios[sid]["criteria"]):
        raise ValueError("Assessment must cover each applicable frozen criterion exactly once")
    for assessment in assessments:
        status = assessment.get("status")
        if status not in ("MET", "NOT_MET", "UNKNOWN"):
            raise ValueError("Applicable criteria cannot be skipped or marked non-applicable")
        text(assessment.get("reason"), "Assessment reason")
        references(assessment.get("evidence"), nonempty=status != "UNKNOWN")
        if coverage != "COMPLETE" and status == "MET":
            raise ValueError("Incomplete method execution cannot establish a successful criterion")
    comparison = run.get("comparison", {})
    if comparison.get("comparability") not in ("COMPARABLE", "UNVERIFIED", "INVALID"):
        raise ValueError("Unknown comparability")
    if changed and comparison["comparability"] != "INVALID":
        raise ValueError("Changed inputs require INVALID comparability: " + ", ".join(changed))
    if (coverage != "COMPLETE" or isolation["status"] != "PASS") and comparison["comparability"] == "COMPARABLE":
        raise ValueError("Missing phases or isolation prevent comparability")
    if comparison.get("decision") not in ("Retain", "Simplify", "Fix", "Unknown"):
        raise ValueError("Unknown scoped decision")
    text(comparison.get("reason"), "Scoped comparison reason")
    references(comparison.get("verification"), nonempty=comparison["decision"] != "Unknown")
    if comparison["comparability"] != "COMPARABLE" and comparison["decision"] != "Unknown":
        raise ValueError("Unverified or invalid comparability requires Unknown")
    return {"valid": True, "id": run["id"], "scenario_id": sid, "condition": condition,
            "coverage": coverage, "comparability": comparison["comparability"], "changed_inputs": changed,
            "limit": "Identity and declared evidence checked; reasoning, isolation and causal benefit are not certified."}


def summarize(series_path, output):
    _, scenarios, config_sha = configuration()
    series = read_json(series_path)
    if not isinstance(series, dict) or series.get("schema") != "qore-eval-series/1":
        raise ValueError("Expected qore-eval-series/1")
    text(series.get("id"), "series id")
    if series.get("scenarios_sha256") != config_sha:
        raise ValueError("Series scenario revision mismatch")
    expected = {(s, c) for s in scenarios for c in CONDITIONS}
    excluded = series.get("excluded_pilot")
    if not isinstance(excluded, list) or len(excluded) > 3:
        raise ValueError("At most one excluded pilot triad is permitted")
    if excluded:
        if len(excluded) != 3 or {p.get("condition") for p in excluded} != set(CONDITIONS) or any(p.get("scenario_id") != "R1" or not p.get("reason") for p in excluded):
            raise ValueError("An excluded pilot must preserve a balanced R1 triad and reasons")
    excluded_results = []
    excluded_ids = set()
    for pilot in excluded:
        if pilot.get("exclusion_basis") not in ("SETUP_CHANGED", "PROTOCOL_CHANGED"):
            raise ValueError("Pilot exclusion requires a setup or protocol change, never outcome selection")
        record_path = contained(series_path.parent, pilot.get("record"))
        if digest(record_path) != pilot.get("sha256"):
            raise ValueError("Excluded pilot record digest mismatch")
        pilot_run = read_json(record_path)
        checked_pilot = check_record(record_path, record_path.parent)
        if pilot_run["scenario_id"] != "R1" or pilot_run["condition"] != pilot["condition"] or pilot_run["id"] in excluded_ids:
            raise ValueError("Excluded pilot identity mismatch or duplicate")
        excluded_ids.add(pilot_run["id"])
        change = pilot.get("change_evidence", {})
        change_path = contained(series_path.parent, change.get("path"))
        if digest(change_path) != change.get("sha256"):
            raise ValueError("Pilot change evidence digest mismatch")
        change_packet = read_json(change_path)
        if not isinstance(change_packet, dict) or change_packet.get("schema") != "qore-eval-change/1" or change_packet.get("kind") != pilot["exclusion_basis"]:
            raise ValueError("Unsupported pilot change evidence")
        before = sha(change_packet.get("before_sha256"), "change before")
        after = sha(change_packet.get("after_sha256"), "change after")
        text(change_packet.get("reason"), "Protocol/setup change reason")
        if before == after:
            raise ValueError("Pilot exclusion requires an actual declared identity change")
        if pilot["exclusion_basis"] == "PROTOCOL_CHANGED":
            old_manifest = read_json(contained(record_path.parent, pilot_run["input_manifest"]))
            if before != old_manifest["scenarios_sha256"] or after != config_sha:
                raise ValueError("Pilot protocol change does not match the before/after revisions")
        elif before != identity(pilot_run["environment"]) or not isinstance(change_packet.get("after_environment"), dict) or after != identity(change_packet["after_environment"]):
            raise ValueError("Pilot setup change does not identify both environments")
        excluded_results.append({**checked_pilot, "record": pilot["record"], "sha256": pilot["sha256"],
                                 "reason": pilot["reason"], "exclusion_basis": pilot["exclusion_basis"], "change_evidence": change,
                                 "limit": "Linked record and change identities checked; a declared change is not proof that exclusion motives were unbiased."})
    cells = series.get("cells")
    if not isinstance(cells, list) or len(cells) != 18:
        raise ValueError("Series must account for all eighteen cells")
    seen, ids, rows = set(), set(excluded_ids), []
    complete = 0
    comparable_groups = {}
    for cell in cells:
        key = (cell.get("scenario_id"), cell.get("condition"))
        if key not in expected or key in seen:
            raise ValueError("Unknown or duplicate series cell")
        seen.add(key)
        records = cell.get("records")
        if not isinstance(records, list) or len(records) > 1:
            raise ValueError("A final-protocol cell has one trial; preserve excluded pilots separately")
        if not records:
            if cell.get("status") != "NOT_RUN":
                raise ValueError("An absent execution must remain NOT_RUN")
            text(cell.get("reason"), "Not-run reason")
            rows.append({"scenario_id": key[0], "condition": key[1], "status": "NOT_RUN", "reason": cell["reason"]})
            continue
        path = contained(series_path.parent, records[0])
        checked = check_record(path, path.parent)
        run = read_json(path)
        run_manifest = read_json(contained(path.parent, run["input_manifest"]))
        if run_manifest["scenarios_sha256"] != config_sha:
            raise ValueError("Final cell uses another protocol revision")
        if (run["scenario_id"], run["condition"]) != key or run["series_id"] != series["id"] or run["id"] in ids:
            raise ValueError("Record is duplicated or belongs to a different series cell")
        ids.add(run["id"])
        if cell.get("status") != checked["coverage"]:
            raise ValueError("Cell status differs from its checked execution")
        complete += checked["coverage"] == "COMPLETE"
        rows.append({**checked, "assessment": run["assessment"], "comparison": run["comparison"]})
        signature = {"candidate": run["candidate_sha256"], "model": run["environment"]["model"],
                     "settings": run["environment"]["settings"], "tools": run["environment"]["tools"]}
        comparable_groups.setdefault(key[0], []).append((signature, checked["comparability"]))
    groups = {}
    for sid in scenarios:
        values = comparable_groups.get(sid, [])
        comparable = len(values) == 3 and all(status == "COMPARABLE" for _, status in values) and len({identity(signature) for signature, _ in values}) == 1
        groups[sid] = {"comparability": "COMPARABLE" if comparable else "UNVERIFIED",
                       "reason": "Matched complete input/model/tool conditions" if comparable else "Missing, invalid or unmatched conditions; no comparative benefit inferred"}
    result = {"schema": "qore-eval-summary/1", "series_id": series["id"], "scenarios_sha256": config_sha,
              "coverage": "COMPLETE" if complete == 18 else ("PARTIAL" if ids - excluded_ids else "BLOCKED"),
              "completed_cells": complete, "planned_cells": 18, "cells": rows, "groups": groups, "excluded_pilot": excluded_results,
              "limit": "One observation per condition on related known tasks. No winner, efficiency or general benefit is inferred."}
    if output.exists() or output.is_symlink():
        raise ValueError("Output exists; choose new staging")
    output.mkdir(parents=True)
    write(output / "summary.json", result)
    lines = ["# Specialization diagnostic", "", "Coverage: " + result["coverage"], "",
             result["limit"], "", "| Scenario | Condition | Execution |", "|---|---|---|"]
    lines += ["| " + r["scenario_id"] + " | " + r["condition"] + " | " + r.get("status", r.get("coverage", "UNKNOWN")) + " |" for r in rows]
    if excluded_results:
        lines += ["", "## Excluded pilot (preserved)", "", "These attempts remain evidence, not final-protocol results.", ""]
        lines += ["- " + r["id"] + " (" + r["condition"] + ", " + r["coverage"] + "): " + r["reason"] + "; record: " + r["record"]
                  for r in excluded_results]
    (output / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    p = commands.add_parser("prepare")
    p.add_argument("--scenario", required=True)
    p.add_argument("--condition", choices=CONDITIONS, required=True)
    p.add_argument("--output", type=Path, required=True)
    p = commands.add_parser("check")
    p.add_argument("record", type=Path)
    p.add_argument("--evidence-root", type=Path)
    p = commands.add_parser("summarize")
    p.add_argument("series", type=Path)
    p.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == "prepare":
            result = prepare(args.scenario, args.condition, args.output)
        elif args.command == "check":
            result = check_record(args.record, args.evidence_root or args.record.parent)
        else:
            result = summarize(args.series, args.output)
        print(json.dumps(result, indent=2))
        return 0
    except (ValueError, OSError, TypeError, KeyError, RecursionError) as error:
        print(json.dumps({"valid": False, "error": str(error)}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
