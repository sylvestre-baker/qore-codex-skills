from pathlib import Path
from datetime import datetime, timezone
import json,hashlib
out=Path('/workspace/output')
candidate='8b26119f383a7d5853c1bd2ab5f678e08966300846c0d6f2784351c1f5a59e8d'
target='0aa277436d8dcda4d6c2412c6ad4307dd0192b0f6230fa96c8b16d99c8bac194'
roles=['product','architecture','ux','delivery','qa']
roster=json.loads((out/'roster.json').read_text())
now=datetime.now(timezone.utc).isoformat()
wrappers={}
for role in roles:
 events=[x for x in roster['events'] if x['role']==role]
 observed=max(x['return_utc'] for x in events)
 meta={'candidate_sha256':candidate,'target_snapshot_sha256':target,'observed_at':observed,'phase_id':role}
 payload={'role':role,'analysis_actor_id':'/root/'+role,'cross_actor_id':next(x['actor_id'] for x in events if x['phase']=='cross_examination'),'events':events,'analysis':(out/f'reports/{role}-analysis.md').read_text(),'cross_examination':(out/f'reports/{role}-cross.md').read_text(),'completed':True,'context_continuity_limit':role in ['product','architecture'],'barrier':roster['analysis_barrier']}
 path=f'evidence/{role}.json';(out/path).write_text(json.dumps({'qore_evidence':meta,'payload':payload},indent=2)+'\n');wrappers[path]=meta
for phase in ['adjudication','spec_validation']:
 meta={'candidate_sha256':candidate,'target_snapshot_sha256':target,'observed_at':now,'phase_id':phase}
 if phase=='adjudication':payload={'actor_id':'/root','report':(out/'evidence/adjudication.md').read_text(),'decisions':['D'+str(i) for i in range(1,10)],'specification':'REPORT.md','basis':'All five initial and cross reports; source comparisons; exact dispositions and dissent retained in REPORT.md.'}
 else:payload={'actor_id':'/root','check':json.loads((out/'evidence/spec-lint.json').read_text()),'meaning':'Structural validation only; no factual or browser certification.'}
 path=f'evidence/{phase}.json';(out/path).write_text(json.dumps({'qore_evidence':meta,'payload':payload},indent=2)+'\n');wrappers[path]=meta
artifacts=[]
excluded={'execution.json','run-check-output.json','validation-final.json'}
for p in sorted(out.rglob('*')):
 if not p.is_file() or p.name in excluded:continue
 rel=str(p.relative_to(out));kind='execution' if rel in wrappers else ('source' if rel.startswith('evidence/source/') or rel=='evidence/input-manifest.json' else 'presentation')
 item={'path':rel,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'kind':kind}
 if kind=='execution':item.update({k:v for k,v in wrappers[rel].items() if k!='phase_id'})
 artifacts.append(item)
phases=[]
for role in roles:
 phases.append({'id':role,'actor_id':'/root/'+role,'cross_actor_id':next(x['actor_id'] for x in roster['events'] if x['role']==role and x['phase']=='cross_examination'),'status':'PASS','artifacts':[f'evidence/{role}.json',f'reports/{role}-analysis.md',f'reports/{role}-cross.md']})
phases += [{'id':'adjudication','actor_id':'/root','status':'PASS','artifacts':['evidence/adjudication.json','evidence/adjudication.md','REPORT.md']},{'id':'spec_validation','actor_id':'/root','status':'PASS','artifacts':['evidence/spec_validation.json','evidence/spec-lint.json','REPORT.md']}]
commands=[]
for filename in ['contract-check.json','spec-lint.json','failed-rg-command.json']:
 data=json.loads((out/'evidence'/filename).read_text());commands.append({'argv':data['argv'],'exit_code':data['exit_code'],'artifact':'evidence/'+filename})
commands.append({'argv':['python3','-B','-'],'exit_code':0,'artifact':'reports/qa-cross.md','note':'Actual child-reported read-only validator counterexample; exact program and stdout retained in full report. Not root re-execution.'})
for p in [out/'evidence/failed-report-probe.json',out/'evidence/run-check-initial.json']:
 if p.exists():
  d=json.loads(p.read_text());commands.append({'argv':d['argv'],'exit_code':d['exit_code'],'artifact':str(p.relative_to(out))})
run={'schema':'qore-run/1','id':'qore003-20261017-p1-generic-1','method':'plan','skill':'qore-plan','candidate_sha256':candidate,'target':{'label':'Frozen prepared-input manifest; change target target/verification-protocol.md','snapshot_sha256':target},'last_relevant_change':'2026-10-17T09:53:58.491824+00:00','environment':{'id':'qore-qualification-qore003-20261017-p1-generic-1','operator':'agent','host':'Docker Desktop Linux arm64 / Codex0.162.0'},'profile':None,'required_phases':roles+['adjudication','spec_validation'],'phases':phases,'artifacts':artifacts,'commands':commands,'limitations':['Planning only; no target edits, browser/network observation, shared-data mutations or current-deployment claims.','Initial Product and Architecture contexts unavailable for follow-up; fresh, explicitly identified continuation contexts performed their one required cross pass; original actor continuity is limited.','Exact host-internal dispatch/return UTC timestamps, token counts and actual billed aggregate agent-seconds unavailable; roster retains observed UTC bounds, completion-file times, notification times and conservative wall occupancy, never fabricated zero.','Enclosing candidate and whole-manifest target digests supplied by user; serialization for independently reproducing enclosing digests not supplied. All inspected input files independently hashed and copied.','Runtime guard coverage, public unanswered indicators, control uniqueness, actual tab/focus behavior, analytics occurrence/effects and deployment identity remain unmeasured.','No project profile exists or was consumed. No review finder/verifier phases required by qore-plan.','Full child reports retained, including command/check observations and QA experiment stdout; original child tool transcripts are not exposed to lead. Root local check output directly captured.','Unavailable rg replaced with supplied local discovery/read methods; failed invocation retained.','Structural validation proves declared structure and identity, not reasoning or factual correctness. Post-seal run-check output retained outside its own digest graph.'],'coverage':'COMPLETE','mode':'Workflow','rounds':{'analysis':1,'cross_examination':1},'stopping_reason':roster['stopping_reason']}
(out/'execution.json').write_text(json.dumps(run,indent=2)+'\n')
print(json.dumps({'execution':str(out/'execution.json'),'artifacts':len(artifacts),'phases':len(phases),'coverage':run['coverage']},indent=2))
