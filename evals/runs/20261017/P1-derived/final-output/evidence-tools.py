from pathlib import Path
import json, datetime, hashlib, subprocess
ROOT=Path("/workspace/output")
META=json.loads((ROOT/"run-metadata.json").read_text())
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def save(name,data):
 p=ROOT/name; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(data,indent=2)); return name
def envelope(phase,payload,path=None):
 return save(path or "evidence/"+phase+".json",{"qore_evidence":{"candidate_sha256":META["candidate_sha256"],"target_snapshot_sha256":META["target_snapshot_sha256"],"observed_at":now(),"phase_id":phase},"payload":payload})
def command(argv,cwd,path):
 start=now(); r=subprocess.run(argv,cwd=cwd,text=True,capture_output=True)
 save(path,{"argv":argv,"cwd":str(cwd),"started_at":start,"returned_at":now(),"exit_code":r.returncode,"stdout":r.stdout,"stderr":r.stderr}); return r
