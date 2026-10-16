"""Independent bounded evidence audit. No browser or external-source execution."""
import json, hashlib, pathlib, subprocess
ROOT=pathlib.Path.cwd().resolve(); OUT=ROOT/'reviewer/RedStone'
def read(p):return json.loads((ROOT/p).read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(v):return (json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False)+'\n').encode()
def save(p,v): (OUT/p).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
req=read('reviewer/RedStone/request.json'); criteria=read('criteria.json'); manifest=read(req['artifact_path'])
checks={}; hashes=[]
checks['canonical_criteria']=sha(canon(criteria))==req['criteria_sha256'] and criteria==req['criteria_snapshot']
checks['manifest_identity']=sha((ROOT/req['artifact_path']).read_bytes())==req['artifact_sha256'] and manifest==req['artifact_descriptors']
names=[f['path'] for f in manifest['files']]; checks['unique_sorted_manifest']=names==sorted(set(names))
for f in manifest['files']:
 p=(ROOT/f['path']).resolve(); ok=p.is_relative_to(ROOT) and p.is_file()
 actual=sha(p.read_bytes()) if ok else None
 hashes.append(dict(path=f['path'],expected=f['sha256'],actual=actual,match=actual==f['sha256']))
checks['all_actual_hashes']=all(f['match'] for f in hashes)
contracts={}; runs={}
for method in criteria['required_check_ids']:
 run=read(f'delivery/evidence/{method}/run.json');runs[method]=run
 cmd=['python3','delivery/tools/run_contract.py',f'delivery/evidence/{method}/run.json']
 c=subprocess.run(cmd,capture_output=True,text=True);contracts[method]=dict(argv=cmd,exit_code=c.returncode,stdout=c.stdout,stderr=c.stderr)
 save(method+'-contract.json',contracts[method])
 checks[method+'_contract']=c.returncode==0
roles=['product','architecture','ux','delivery','qa']; roles_audit=[]
for role in roles:
 base=ROOT/'delivery/evidence/plan';a=(base/'analyze'/f'{role}.md').read_text();c=(base/'challenge'/f'{role}.md').read_text();env=read(f'delivery/evidence/plan/phase-{role}.json')
 roles_audit.append(dict(role=role,analysis_bytes=len(a.encode()),challenge_bytes=len(c.encode()),payload_keys=list(env['payload']),profile_mentioned='profile' in a.lower(),challenge_has_peer_references=all(x.lower() in c.lower() for x in roles)))
checks['plan_roles']=len({p['actor_id'] for p in runs['plan']['phases'] if p['id'] in roles})==5 and all(r['analysis_bytes']>1000 and r['challenge_bytes']>1000 and r['profile_mentioned'] and r['challenge_has_peer_references'] for r in roles_audit)
gates=read('delivery/evidence/ux/gate-evidence.json'); gate_audit={}
for key,v in gates.items():
 gate_audit[key]=dict(observation=v['observation'],evidence=v['evidence'],contained_available=all((ROOT/'delivery/evidence/ux'/p).is_file() for p in v['evidence']))
checks['ux_gates']=set(gates)=={f'G{i}' for i in range(7)} and all(v['contained_available'] for v in gate_audit.values())
events=read('delivery/evidence/ux/iteration-1-journey/events.json');actions=events['actions']
checks['ux_actual_transitions']=sum(a['type']=='assert-none-checked' for a in actions)==3 and any(a['type']=='focus-step' and a.get('active_element',{}).get('text')=='Back' and a.get('reached') for a in actions) and all(any(a['type']=='assert-focused' and a.get('selector')==s for a in actions) for s in ['summary','h1']) and any(a['type']=='assert-hidden' and a.get('selector')=='summary' for a in actions)
review=runs['review'];finders=[p['actor_id'] for p in review['phases'] if p['id'].startswith('finder.')]; verifier=next(p['actor_id'] for p in review['phases'] if p['id']=='verifier')
checks['review_independent_roles']=len(finders)==len(set(finders))==3 and verifier not in finders
profile_use={role:read(f'delivery/evidence/review/finders/{role}/profile-use.json') for role in ['correctness','security','feasibility']}
checks['review_profile']=all(p['profile']['sha256']==review['profile']['sha256'] for p in profile_use.values())
redaction=read('delivery/evidence/review/redaction.json');checks['mechanical_filter']=redaction['exit']==0 and '5 claims' in redaction['stderr']
original=read('delivery/evidence/review/verified.json')['findings']; fixes=read('delivery/evidence/review/fix-verifier/results.json')
checks['original_severity_preserved']=len(original)==5 and all(f['severity']=='medium' and f['verdict']=='CONFIRMED' for f in original) and all(f['severity']=='medium' and f['original_verdict']=='CONFIRMED' for f in fixes['findings'])
checks['fix_identity']=all(sha((ROOT/'delivery'/p).read_bytes())==fixes['sha256'][p] for p in ['tools/coordination.py','tools/agent_mail.py'])
checks['separate_fix_checks']=len(fixes['checks'])==7 and all(c['status']=='PASS' for c in fixes['checks'])
limitations=["This reviews delivered execution evidence; no browser rerun, original agent reasoning certification, defect-absence assertion or release approval.","Raw private traces/video, unselected screenshots and original CLI transcripts are unavailable here; selected transformations and provenance are the available evidence.","Planning and phase independence are supported by saved reports/context identities, not independently reconstructed internal reasoning.","Linux collected 149 tests: 138 passed, 11 optional browser tests skipped; dated macOS observations are separate.","Post-fix test/doc hashes are recorded but those current test/doc bytes and adjacent suite logs are not included in this manifest; current delivered helper hashes match. Fix checks were inspected, not rerun.","ACK fix establishes scheduling-budget behavior only; no absolute OS deadline or real-network timing certification."]
base={k:req[k] for k in ['task_id','task_revision','criteria_sha256','artifact_revision','artifact_sha256','delivery_message_id','review_request_id','review_session_id','review_run_id']}
notes={'plan':'Five distinct roles have substantial Analyze and cross-examination outputs, shared-report barrier and concrete adjudication. Profile selected offline checker and separate Close/Back/unanswered obligations; nine-scenario result retained. Planning does not establish website behavior.','ux':'G0-G6 map to contained selected evidence. Actual dated action events include sequential Tab, Enter/Space/reopen/Close, separate summary and heading focus, three unanswered assertions, returned introduction and direct/reload/history neighbors. Expected blocked analytics and scope exclusions are explicit. No browsers rerun.','review':'Three distinct finder identities, actual five-claim mechanical filter and separate fresh verifier with independently authored reproduction outputs are retained. Five medium IDs/four defects remain CONFIRMED; separate current fixes are RESOLVED only within focused scope. Original archive, normalized snapshot and post-fix helper identities are distinct.'}
common=all(checks[k] for k in ['canonical_criteria','manifest_identity','unique_sorted_manifest','all_actual_hashes'])
proofs=[]
for method,keys in {'plan':['plan_contract','plan_roles'],'ux':['ux_contract','ux_gates','ux_actual_transitions'],'review':['review_contract','review_independent_roles','review_profile','mechanical_filter','original_severity_preserved','fix_identity','separate_fix_checks']}.items():
 result='PASS' if common and all(checks[k] for k in keys) else 'FAIL'
 record=dict(base,check_id=method,result=result,reviewer='RedStone',method_run_id=runs[method]['id'],evidence_assessment=notes[method],checks={k:checks[k] for k in keys},limitations=limitations)
 name=method+'-proof.json';save(name,record);proofs.append(dict(check_id=method,path='reviewer/RedStone/'+name,sha256=sha((OUT/name).read_bytes())))
results=dict(checks=checks,file_hashes=hashes,roles=roles_audit,gates=gate_audit,contracts=contracts,limitations=limitations)
save('results.json',results)
verdict=dict(base,kind='review_verdict',verdict='PASS' if all(checks.values()) else 'FAIL',proofs=proofs,summary=notes,limitations=limitations)
save('verdict.json',verdict)
print(json.dumps({'checks':checks,'files_checked':len(hashes),'verdict':verdict['verdict'],'proofs':proofs},indent=2))
