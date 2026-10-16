import hashlib,json,pathlib,subprocess,datetime
out=pathlib.Path('/workspace/qualification/finders/security'); root=pathlib.Path('/workspace/project'); skill=root/'examples/qaizen-labs/.agents/skills/qore-review-qaizen-labs'
commands=[(skill,['python3','scripts/project-check.py','references/project.json','--root',str(root/'examples/qaizen-labs'),'--method','review']), (root/'examples/qaizen-labs',['python3','-B','checks/check_contract.py','surface-contract.json'])]
commands += [(root,['python3','-B','-m','unittest','discover','-s','tests','-p',p,'-v']) for p in ['test_task_gate.py','test_coordination.py','test_agent_mail.py','test_labs_contract.py','test_browser_probe.py']]
commands += [(root,['node','--check','tools/browser_probe.mjs'])]
results=[]
for cwd,argv in commands:
 r=subprocess.run(argv,cwd=cwd,capture_output=True,text=True)
 results.append(dict(cwd=str(cwd),argv=argv,exit_code=r.returncode,stdout=r.stdout,stderr=r.stderr,observed_at=datetime.datetime.now(datetime.timezone.utc).isoformat()))
(out/'commands.json').write_text(json.dumps(results,indent=2)+'\n')
(out/'preflight.json').write_text(results[0]['stdout'])
paths=['examples/qaizen-labs/'+p for p in ['verification-spec.md','surface-contract.json','checks/check_contract.py','browser-actions.json','observation-policy.json','README.md']]
paths += ['tools/'+p for p in ['browser_probe.mjs','task_gate.py','coordination.py','agent_mail.py','context.py']]
paths += ['tests/'+p for p in ['test_task_gate.py','test_coordination.py','test_agent_mail.py','test_labs_contract.py','test_browser_probe.py','fixtures/keyboard-journey.html']]
paths += ['docs/coordination.md','docs/coordination-dependencies.md']
def manifest(base, names):
 return [{'path':str(p),'sha256':hashlib.sha256((base/p).read_bytes()).hexdigest()} for p in sorted(names)]
target=manifest(root,paths)
candidate=manifest(skill,[str(p.relative_to(skill)) for p in skill.rglob('*') if p.is_file() and '__pycache__' not in str(p)])
for name,data in [('target-manifest',target),('skill-manifest',candidate)]:
 raw=(json.dumps(data,sort_keys=True,separators=(',',':'))+'\n').encode(); (out/(name+'.json')).write_bytes(raw)
 print(name,hashlib.sha256(raw).hexdigest())
