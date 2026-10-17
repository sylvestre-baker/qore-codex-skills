#!/usr/bin/env python3
"""Stage only the explicitly selected static showcase; never deploy it."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]

def build(output):
    if output.exists(): raise ValueError("Output exists; choose new staging")
    selected = [(ROOT / "showcase/index.html", "index.html"), (ROOT / "showcase/styles.css", "styles.css")]
    selected += [(ROOT / "profiles/qaizen-labs.json", "profiles/qaizen-labs.json"),
                 (ROOT / "docs/showcase.md", "reference/showcase.md"),
                 (ROOT / "docs/coordination-dependencies.md", "reference/coordination-dependencies.md")]
    for base, target in ((ROOT / "docs/demo/qaizen-labs", "media"), (ROOT / "docs/evidence/qaizen-labs", "evidence")):
        for path in sorted(base.rglob("*")):
            if path.is_symlink(): raise ValueError("Symlinks are refused")
            if path.is_file(): selected.append((path, str(Path(target) / path.relative_to(base))))
    if not any(name == "media/demo.mp4" for _, name in selected): raise ValueError("Demonstration is unavailable")
    if sum(p.stat().st_size for p, _ in selected) > 35 * 1024 * 1024: raise ValueError("Site exceeds 35 MiB")
    records = []
    for source, rel in selected:
        dest = output / rel; dest.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(source, dest)
        if rel in ("media/transcript.md", "media/transcript.html"):
            dest.write_text(dest.read_text().replace("../../evidence/qaizen-labs/", "../evidence/"))
        if rel == "evidence/README.md":
            text = dest.read_text().replace("../../../profiles/", "../profiles/")
            text = text.replace("../../demo/qaizen-labs/", "../media/")
            text = text.replace("../../showcase.md", "../reference/showcase.md")
            text = text.replace("../specialization/README.md", "https://github.com/sylvestre-baker/qore-codex-skills/blob/41f1355de4686d9014557b17997edfb375af25d3/docs/evidence/specialization/README.md")
            dest.write_text(text.replace("../../coordination-dependencies.md", "../reference/coordination-dependencies.md"))
        records.append({"path": rel, "sha256": hashlib.sha256(dest.read_bytes()).hexdigest(), "source": str(source.relative_to(ROOT)),
                        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                        "transformation": "Evidence links rebased for static staging" if rel.startswith("media/transcript.") or rel == "evidence/README.md" else "Exact bytes"})
    (output / ".nojekyll").write_text("")
    (output / "site-manifest.json").write_text(json.dumps({"schema":"qore-static-site/1","files":records,"publication":"NOT_DEPLOYED_BY_BUILD"},indent=2)+"\n")
    return {"output":str(output),"files":len(records),"bytes":sum(p.stat().st_size for p, _ in selected),"deployed":False}

if __name__ == "__main__":
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument("--output",type=Path,required=True)
    try: print(json.dumps(build(parser.parse_args().output),indent=2))
    except (ValueError,OSError) as error: parser.exit(1,str(error)+"\n")
