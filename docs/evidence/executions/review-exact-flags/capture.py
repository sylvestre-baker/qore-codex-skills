from pathlib import Path
import hashlib,json,subprocess,datetime,platform,shutil,zipfile
r=Path('/workspace/qore-skills-0.1.0'); e=Path('/workspace/review-evidence')
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def run(name,argv,cwd=r):
 t=datetime.datetime.now(datetime.timezone.utc).isoformat(); p=subprocess.run(argv,cwd=cwd,capture_output=True,text=True,timeout=180)
 o=dict(argv=argv,cwd=str(cwd),exit_code=p.returncode,stdout=p.stdout,stderr=p.stderr,observed_at=t)
 (e/(name+'.json')).write_text(json.dumps(o,indent=2)); return o
files=[p for p in r.rglob('*') if p.is_file() and '.git' not in p.parts and not any('auth' in s.lower() for s in p.parts)]
manifest=[]
for p in sorted(files):
 rel=p.relative_to(r); dest=e/'snapshot'/rel; dest.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(p,dest)
 manifest.append(dict(path=str(rel),sha256=digest(p),mtime=p.stat().st_mtime))
(e/'snapshot-manifest.json').write_text(json.dumps(manifest,indent=2))
targethash=digest(e/'snapshot-manifest.json')
archive=Path('/workspace/candidate.zip'); ah=digest(archive)
with zipfile.ZipFile(archive) as z:
 checks=[]
 for p in files:
  rel=str(p.relative_to(r)); matches=[n for n in z.namelist() if n==rel or n.endswith('/'+rel)]
  if len(matches)==1: checks.append(dict(path=rel,match=hashlib.sha256(z.read(matches[0])).hexdigest()==digest(p)))
(e/'identity.json').write_text(json.dumps(dict(candidate_sha256=ah,expected_candidate_sha256='bafd0da80667a00f9e6bd2f9e726eaa64d61ff42d026b9f58eb857df15bf40f8',target_snapshot_sha256=targethash,procedure='SHA256 raw archive; target SHA256 snapshot-manifest.json bytes; per-file SHA256 and copy2 snapshots; matching ZIP member byte comparisons',archive_checks=checks,last_relevant_change=datetime.datetime.fromtimestamp(max(p.stat().st_mtime for p in files),datetime.timezone.utc).isoformat(),environment=dict(id='independent-linux-container',operator='agent',host=platform.platform())),indent=2))
run('capabilities',['sh','-c','command -v python3; command -v node; command -v bash; command -v rg; uname -a'])
run('project-tests',['python3','-B','-m','unittest','discover','-s','tests','-v'])
(e/'empty.json').write_text('{"findings": []}\n')
for variant in ['skills','.agents/skills']:
 run('malformed-verifier-'+variant.replace('/','-'),['node',str(r/variant/'qore-review/scripts/finding-lint.mjs'),str(e/'empty.json'),'--verifier=ran=skipped','--json'])
(e/'source-unchanged.json').write_text(json.dumps({'unchanged':all(digest(r/x['path'])==x['sha256'] for x in manifest)},indent=2))
