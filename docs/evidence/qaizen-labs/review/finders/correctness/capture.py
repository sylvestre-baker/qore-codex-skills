from pathlib import Path
import subprocess, json, hashlib, datetime, shutil
root=Path('/workspace/project'); out=Path('/workspace/qualification/finders/correctness'); example=root/'examples/qaizen-labs'; skill=example/'.agents/skills/qore-review-qaizen-labs'
commands=[('preflight', ['python3',str(skill/'scripts/project-check.py'),str(skill/'references/project.json'),'--root',str(example),'--method','review'],example),('contract',['python3','-B','checks/check_contract.py','surface-contract.json'],example)]
for name in ('coordination','agent_mail','task_gate','labs_contract','browser_probe'):
 commands.append((name,['python3','-B','-m','unittest','discover','-s','tests','-p','test_'+name+'.py','-v'],root))
commands.append(('node-syntax',['node','--check','tools/browser_probe.mjs'],root))
records=[]
for name,argv,cwd in commands:
 p=subprocess.run(argv,cwd=cwd,capture_output=True,text=True)
 rec={'argv':argv,'cwd':str(cwd),'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'observed_at':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 (out/(name+'.json')).write_text(json.dumps(rec,indent=2)+'\n');records.append({'name':name,'exit_code':p.returncode,'artifact':name+'.json'})
(out/'commands.json').write_text(json.dumps(records,indent=2)+'\n')
paths=[example/x for x in ['verification-spec.md','surface-contract.json','checks/check_contract.py','browser-actions.json','observation-policy.json','README.md']]
paths += [root/x for x in ['tools/browser_probe.mjs','tools/task_gate.py','tools/coordination.py','tools/agent_mail.py','tests/test_browser_probe.py','tests/test_task_gate.py','tests/test_coordination.py','tests/test_agent_mail.py','tests/test_labs_contract.py','tests/fixtures/keyboard-journey.html']]
paths += sorted((root/'docs').glob('coordination*.md'))
manifest=[]
for p in paths:
 rel=p.relative_to(root); data=p.read_bytes(); dest=out/'snapshot'/rel;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
 manifest.append({'path':str(rel),'sha256':hashlib.sha256(data).hexdigest(),'mtime':datetime.datetime.fromtimestamp(p.stat().st_mtime,datetime.timezone.utc).isoformat()})
raw=(json.dumps(manifest,sort_keys=True,indent=2)+'\n').encode();(out/'snapshot-manifest.json').write_bytes(raw)
candidate=[{'path':str(p.relative_to(skill)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(skill.rglob('*')) if p.is_file() and '__pycache__' not in str(p)]
craw=(json.dumps(candidate,sort_keys=True,indent=2)+'\n').encode();(out/'candidate-manifest.json').write_bytes(craw)
(out/'identity.json').write_text(json.dumps({'target_snapshot_sha256':hashlib.sha256(raw).hexdigest(),'candidate_sha256':hashlib.sha256(craw).hexdigest(),'procedure':'SHA-256 of saved sorted-key JSON manifest bytes (indent 2 plus LF); each manifest entry hashes actual file bytes. Target source copies retained. Git HEAD unavailable: unborn repository with untracked source.','last_relevant_change':max(x['mtime'] for x in manifest)},indent=2)+'\n')
