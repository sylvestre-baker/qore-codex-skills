from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
out=Path('/workspace/output');now=datetime.now(timezone.utc).isoformat()
candidate='8b26119f383a7d5853c1bd2ab5f678e08966300846c0d6f2784351c1f5a59e8d';target='92981d42bbb636d2809b22af476c7974c1a1f54b539b8e5a7d6c9767b0d53b1d'
def read(p):return (out/p).read_text()
def obj(p):return json.loads(read(p))
roster=obj('roster.json');phases=[]
phase_dir=out/'evidence/phases';phase_dir.mkdir(exist_ok=True)
def phase(pid,actor,payload,refs,observed=now):
 rel=f'evidence/phases/{pid}.json';identity={'candidate_sha256':candidate,'target_snapshot_sha256':target,'observed_at':observed,'phase_id':pid}
 (out/rel).write_text(json.dumps({'qore_evidence':identity,'payload':payload},indent=2))
 phases.append({'id':pid,'actor_id':actor,'status':'PASS','artifacts':[rel]+refs})
phase('profile_preflight','/root',{'argv':['python3','-B','.agents/skills/qore-plan-qaizen-labs/scripts/project-check.py','.agents/skills/qore-plan-qaizen-labs/references/project.json','--root','/workspace/worker','--method','plan'],'cwd':'/workspace/worker','exit_code':0,'result':obj('evidence/profile-check.json'),'consumption':obj('evidence/profile-use.json')},['evidence/profile-check.json','evidence/profile-use.json'],'2026-10-17T11:30:54.605766+00:00')
for role in ['product','architecture','ux','delivery','qa']:
 a=next(a for a in roster['actors'] if a['role']==role and a.get('phase')!='cross');cross=next((x for x in roster['actors'] if x['role']==role and x.get('phase')=='cross'),a)
 refs=[f'reports/{role}-analysis.md',f'reports/{role}-cross.md',f'reports/{role}-claims.json','evidence/analysis-barrier.json','evidence/cross-barrier.json','roster.json']
 phase(role,a['actor_id'],{'initial_actor':a['actor_id'],'cross_actor':cross['actor_id'],'analysis_report':read(refs[0]),'cross_report':read(refs[1]),'claims':obj(refs[2]),'analysis_return_observed_utc':a['initial_return_utc'],'cross_return_observed_utc':cross['cross_return_utc'],'continuity_limitation':a.get('context_continuity'),'barrier':obj('evidence/analysis-barrier.json')},refs,cross['cross_return_utc'])
phase('claim_filter','/root',{'transformation':obj('evidence/filter-log.json'),'all_filtered_claims':obj('evidence/filtered-claims.json'),'script':read('evidence/filter-claims.py')},['evidence/filter-log.json','evidence/filtered-claims.json','evidence/filter-claims.py'],obj('evidence/filter-log.json')['observed_at'])
v=next(x for x in roster['actors'] if x['role']=='verifier')
phase('verifier','/root/verifier',{'report':read('reports/verifier.md'),'results':obj('reports/verifier-results.json'),'context':'Fresh fork_turns=none. Only mechanically filtered claim fields and listed original sources; no role full reports, lead plan or candidate wording.','deadline':v['deadline_request']},['reports/verifier.md','reports/verifier-results.json','evidence/filtered-claims.json','evidence/filter-log.json'],v['return_utc'])
phase('adjudication','/root',{'adjudication':obj('evidence/adjudication.json'),'final_specification':read('REPORT.md'),'proposed_documentation':read('proposed-protocol.md'),'mode':obj('evidence/method-selection.json'),'verifier_limits_retained':'No independent verifier proof of earlier checker run; actual lead run output retained separately. Effort, counting/outcome labels and redirects are proposed, not measured.'},['evidence/adjudication.json','REPORT.md','proposed-protocol.md','evidence/method-selection.json'])
phase('contract_check','/root',{'argv':['python3','-B','checks/check_contract.py','surface-contract.json'],'cwd':'/workspace/worker','exit_code':0,'stdout':read('evidence/contract-check.json'),'limit':'Contract consistency only; no website contacted.'},['evidence/contract-check.json'],'2026-10-17T11:30:54.605766+00:00')
phase('input_integrity','/root',obj('evidence/input-immutability.json'),['evidence/input-immutability.json','evidence/input-manifest.json'],obj('evidence/input-immutability.json')['observed_at'])
phase('spec_validation','/root',{'argv':['bash','scripts/spec-lint.sh','/workspace/output/REPORT.md'],'cwd':'/workspace/worker/.agents/skills/qore-plan-qaizen-labs','exit_code':0,'stdout':read('evidence/spec-lint.txt'),'validated_spec_sha256':hashlib.sha256((out/'REPORT.md').read_bytes()).hexdigest(),'interpretation':'Structural validity only, not reasoning correctness.'},['REPORT.md','evidence/spec-lint.txt'])
artifacts=[]
for p in sorted(out.rglob('*')):
 if not p.is_file() or p.name=='execution.json' or p.name.startswith('run-check') or p.name.startswith('validation-summary'):continue
 rel=str(p.relative_to(out));a={'path':rel,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'kind':'source' if rel.startswith('sources/') else 'presentation'}
 if p.parent==phase_dir:
  meta=json.loads(p.read_text())['qore_evidence'];a.update({k:meta[k] for k in ['candidate_sha256','target_snapshot_sha256','observed_at']});a['kind']='execution'
 artifacts.append(a)
commands=[{'argv':['sh','-c',"pwd && rg --files -g 'TASK.md' -g 'AGENTS.md' -g '*SKILL*' -g '*qore*' -g '*manifest*'"],'exit_code':127,'artifact':'evidence/operations.json'},
 {'argv':['find','/workspace/output/reports','-maxdepth','1','-type','f','-printf','%f\\n'],'exit_code':1,'artifact':'evidence/operations.json'},
 {'argv':['python3','-B','.agents/skills/qore-plan-qaizen-labs/scripts/project-check.py','.agents/skills/qore-plan-qaizen-labs/references/project.json','--root','/workspace/worker','--method','plan'],'exit_code':0,'artifact':'evidence/phases/profile_preflight.json'},
 {'argv':['python3','-B','checks/check_contract.py','surface-contract.json'],'exit_code':0,'artifact':'evidence/phases/contract_check.json'},
 {'argv':['python3','-B','/workspace/output/evidence/filter-claims.py'],'exit_code':0,'artifact':'evidence/phases/claim_filter.json'},
 {'argv':['bash','scripts/spec-lint.sh','/workspace/output/REPORT.md'],'exit_code':0,'artifact':'evidence/phases/spec_validation.json'}]
run={'schema':'qore-run/1','id':'qore003-20261017-p2-derived-1','method':'plan','skill':'qore-plan-qaizen-labs','candidate_sha256':candidate,'target':{'label':'Frozen prepared-input manifest for verification-protocol documentation clarification','snapshot_sha256':target},'last_relevant_change':'2026-10-17T09:53:58.874712+00:00','environment':{'id':'qore-qualification-qore003-20261017-p2-derived-1','operator':'agent','host':'Docker Desktop Linux arm64 / Codex0.162.0'},'profile':{'id':'qaizen-labs','version':'0.1.0','sha256':'f76afdd45cb6352e5044a06affc4182ea6cd40aa9c012fb216636a61faa428f0'},'required_phases':[p['id'] for p in phases],'phases':phases,'artifacts':artifacts,'commands':commands,'limitations':[
'No network/browser execution. Actual deployment behavior, DOM/tab order/focus, guard enforcement, unanswered representation and analytics effects unobserved; not required for documentation planning.',
'Original Product and UX contexts retired by runtime; fresh explicitly named cross contexts used complete saved own/peer reports. All five independent initial roles and all challenge links ran.',
'Host provides canonical context names but no per-agent usage metrics or exact dispatch/completion timestamps. Roster preserves observed UTC intervals; actual usage is unavailable, never zero. Some conservative cross spans exceed role deadlines; expiry requests were not sent before already-complete notifications at next scheduling boundary.',
'Enclosing candidate/target identities supplied by user. Per-file manifest and full supplied snapshots retained; enclosing digest canonicalization was not available for independent recomputation.',
'Verifier could not independently substantiate prior successful checker-run claims because command outputs excluded from its permitted context. Lead retained actual executed command output separately; verifier qualifications preserved.',
'Delivery effort estimate unmeasured. Counting convention, canonical/alternative evidence labels, outcome taxonomy and redirect coverage are proposals, not observed facts or source-defined result schema.',
'Impact-severity disagreements and corrected/refuted claims preserved in full initial/cross reports and filtered claims; no average or comparative winner manufactured.',
'Only supplied project scope inspected. No claims about unsupplied consumers, private source, other projects or general accessibility certification.',
'rg unavailable; BusyBox find rejected -printf; failed commands retained and standard read/search fallbacks used.',
'Structural validators check structure and declared identity/coverage, not reasoning correctness. Final run-check result is a separate companion to avoid circular artifact self-hashing.'
],'coverage':'COMPLETE'}
(out/'execution.json').write_text(json.dumps(run,indent=2));print(json.dumps({'phases':len(phases),'artifacts':len(artifacts),'coverage':'COMPLETE','created_at':now}))
