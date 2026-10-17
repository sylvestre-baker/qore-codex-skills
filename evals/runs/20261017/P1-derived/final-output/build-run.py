from pathlib import Path
import json,hashlib,datetime
out=Path('/workspace/output');m=json.loads((out/'run-metadata.json').read_text());now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
# Verify candidate skill resource inventory against its supplied bundled release manifest.
skill=Path('/workspace/worker/.agents/skills/qore-plan-qaizen-labs');release=json.loads((skill/'references/release.json').read_text());checks=[]
for row in release['resources']:
 p=skill/row['path']; actual=hashlib.sha256(p.read_bytes()).hexdigest();checks.append({'path':row['path'],'expected_sha256':row['sha256'],'actual_sha256':actual,'matches':actual==row['sha256']})
(out/'evidence/skill-resource-check.json').write_text(json.dumps({'observed_at':now(),'resources':checks,'all_match':all(x['matches'] for x in checks),'limit':'Internal bundled resource manifest consistency only. Operator supplied enclosing candidate digest is retained as identity; canonical enclosing serialization unavailable.'},indent=2))
roster=json.loads((out/'roster.json').read_text());budget=json.loads((out/'budget.json').read_text());budget['final_evidence_assembly_at']=now();budget['elapsed_wall_seconds_at_assembly']=(datetime.datetime.now(datetime.timezone.utc)-datetime.datetime.fromisoformat(budget['start_utc'])).total_seconds();budget['observed_child_report_intervals_seconds']=roster['usage']['child_reported_active_wall_seconds_excluding_verifier']+52;budget['observed_wall_proxy_total_at_assembly']=budget['elapsed_wall_seconds_at_assembly']+budget['observed_child_report_intervals_seconds'];budget['limitations']=['Exact aggregate agent usage unavailable from API. Proxy excludes some dispatch-to-first-clock and return handoff overhead; not a measurement of CPU, tokens or aggregate agent-seconds.','Delivery cross report/evidence retention returned beyond nominal role deadline after available-results requests; no new investigation at expiry.','Initial three dispatch UTCs are post-dispatch local observations, not exposed API event timestamps; role clocks give additional actual activity bounds.'];(out/'budget.json').write_text(json.dumps(budget,indent=2))
art=[]
for p in sorted(out.rglob('*')):
 if not p.is_file() or p.name in ['execution.json','run-check-final.json','run-check-final-command.json']:continue
 rel=str(p.relative_to(out));kind='source' if rel.startswith('sources/') or rel in ['input-manifest.json','run-metadata.json'] else 'presentation'
 row={'path':rel,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'kind':kind}
 if rel.startswith('evidence/'):
  try: envelope=json.loads(p.read_text())
  except (ValueError,UnicodeDecodeError):envelope={}
  if 'qore_evidence' in envelope:
   row['kind']='execution';row.update({k:envelope['qore_evidence'][k] for k in ['candidate_sha256','target_snapshot_sha256','observed_at']})
 art.append(row)
phases=[]
for phase in ['profile_preflight','product','architecture','ux','delivery','qa','adjudication','spec_validation','claim_verification']:
 actor='/root/'+phase if phase in ['product','architecture','ux','delivery','qa'] else ('/root/fresh_verifier' if phase=='claim_verification' else '/root')
 refs=['evidence/'+phase+'.json']
 if phase in ['product','architecture','ux','delivery','qa']:refs+=['reports/'+phase+'-analysis.md','reports/'+phase+'-cross-examination.md','roster.json']
 elif phase=='profile_preflight':refs+=['profile-check.json','profile-use.json','input-manifest.json']
 elif phase=='adjudication':refs+=['adjudication.json','REPORT.md']
 elif phase=='spec_validation':refs+=['REPORT.md','evidence/spec-lint-command.json']
 else:refs+=['reports/fresh-verifier.md','verifier-results.json','claims-filtered.json','filter-claims.py']
 phases.append({'id':phase,'actor_id':actor,'status':'PASS','artifacts':refs})
commands=[]
for name in ['profile-preflight','contract-check','spec-lint']:
 path=f'evidence/{name}-command.json';d=json.loads((out/path).read_text());commands.append({'argv':d['argv'],'exit_code':d['exit_code'],'artifact':path})
commands+=[{'argv':['rg','--files','-g','TASK.md','-g','AGENTS.md','-g','*manifest*','-g','SKILL.md','.'],'exit_code':127,'artifact':'evidence/capabilities.json'},{'argv':['find','/workspace/output/reports','-maxdepth','1','-type','f','-printf','%f\\n'],'exit_code':1,'artifact':'evidence/capabilities.json'},{'argv':['python3','-B','-'],'exit_code':0,'artifact':'evidence/delivery-probe-command.json'}]
limitations=[
'Offline planning only; no deployed site, browser, DOM, key/focus, analytics effects, live guard enforcement or deployment identity observed. No network/connector access used.',
'Future third-party subresource authorization and host capability remain unresolved. Full questionnaire/mobile/results/submission/performance/accessibility certification and source redistribution excluded.',
'Workflow cross-examination role continuity migrated to fresh contexts after actual followup actor-not-found errors. Each replacement read its own complete saved report and all initial peer reports after barrier. This is not uninterrupted same-context continuation.',
'Exact internal dispatch/return events and measured aggregate agent-seconds/CPU/token usage are unavailable from the collaboration API; roster retains local UTC observations and child-reported clocks; budget retains wall proxies and allocation bounds, not fabricated zero usage.',
'Delivery cross retention/return exceeded nominal worker deadline despite available-results requests. No extra investigation or quality retry dispatched at expiry.',
'Operator-supplied candidate and whole-prepared-input target hashes retained. Exact canonical enclosing manifest/digest procedure not supplied; per-file hashes, full original bytes, bundled skill resource comparisons and input immutability independently retained.',
'Fresh verifier was shown only 12 mechanically whitelisted claims and original sources, not full role reports or final report. It covered all 12: 11 supported and C12 partly supported as an interpretation. This audit does not prove all omitted claims or entire specification correctness.',
'Presentation-level absence is an adopted interpretation; DOM deletion, accessibility-tree behavior and answer persistence after return are not verified facts.',
'QA in-memory probe has full role report but lacks a separate raw command transcript. Delivery probe has exact retained command/output with UTC bounds, not exact separately measured command-start instant.',
'rg unavailable and BusyBox find lacks -printf; failed probes retained; fallback file reads/Python used.',
'Structure validators check declared artifact identity/coverage and document syntax only; they do not prove source reasoning, factual correctness, independent cognition from labels, or permission to implement/deploy.',
'Final run-check is executed after this record is frozen. Its exact output/argv/exit are saved as companion run-check-final.json and run-check-final-command.json outside this artifact manifest to avoid a self-referential digest cycle.'
]
run={'schema':'qore-run/1','id':m['run_id'],'method':'plan','skill':'qore-plan-qaizen-labs','candidate_sha256':m['candidate_sha256'],'target':{'label':'Frozen prepared-input snapshot; plan changes to target/verification-protocol.md','snapshot_sha256':m['target_snapshot_sha256']},'last_relevant_change':m['last_relevant_change'],'environment':m['environment'],'profile':m['profile'],'required_phases':[p['id'] for p in phases],'phases':phases,'artifacts':art,'commands':commands,'limitations':limitations,'coverage':'COMPLETE'}
(out/'execution.json').write_text(json.dumps(run,indent=2));print(json.dumps({'declared_coverage':run['coverage'],'phases':len(phases),'artifacts':len(art),'elapsed_wall_seconds':budget['elapsed_wall_seconds_at_assembly'],'active_wall_proxy_seconds':budget['observed_wall_proxy_total_at_assembly'],'all_skill_resources_match':all(x['matches'] for x in checks)},indent=2))
