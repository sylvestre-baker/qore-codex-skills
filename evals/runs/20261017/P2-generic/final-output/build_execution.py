from pathlib import Path
import datetime, hashlib, json
out=Path('/workspace/output')
meta=json.loads((out/'evidence/run-metadata.json').read_text())
roster=json.loads((out/'roster.json').read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def timestamp(p):return datetime.datetime.fromtimestamp(p.stat().st_mtime,datetime.timezone.utc).isoformat()
phases=[]
for row in roster['actual_contexts']:
 role=row['role']; ap=out/row['initial']['report']; cp=out/row['cross_examination']['report']
 identity={'candidate_sha256':meta['candidate_sha256'],'target_snapshot_sha256':meta['target_snapshot_sha256'],'observed_at':timestamp(cp),'phase_id':role}
 payload={'role':role,'initial_actor_id':row['actor_id'],'cross_examination_actor_id':row['cross_examination']['actor_id'],'initial_report':{'path':str(ap.relative_to(out)),'sha256':sha(ap),'full_output':ap.read_text()},'cross_examination_report':{'path':str(cp.relative_to(out)),'sha256':sha(cp),'full_output':cp.read_text()},'timing':row,'barrier':'evidence/report-barrier.json','stopping_reason':'One Analyze and one Cross-examine pass per role completed; lead adjudication follows. No extra quality retry.'}
 ep=out/'evidence'/f'phase-{role}.json';ep.write_text(json.dumps({'qore_evidence':identity,'payload':payload},indent=2))
 phases.append({'id':role,'actor_id':row['actor_id'],'status':'PASS','artifacts':[str(ep.relative_to(out)),str(ap.relative_to(out)),str(cp.relative_to(out))]})
for phase,name in [('adjudication','adjudication.md')]:
 p=out/name;ep=out/'evidence'/f'phase-{phase}.json'; ep.write_text(json.dumps({'qore_evidence':{'candidate_sha256':meta['candidate_sha256'],'target_snapshot_sha256':meta['target_snapshot_sha256'],'observed_at':timestamp(p),'phase_id':phase},'payload':{'actor_id':'/root','full_output':p.read_text(),'report':name}},indent=2))
 phases.append({'id':phase,'actor_id':'/root','status':'PASS','artifacts':[str(ep.relative_to(out)),name,'specification.md','proposed-verification-protocol.md']})
phases.append({'id':'spec_validation','actor_id':'/root','status':'PASS','artifacts':['evidence/phase-spec_validation.json','evidence/spec-lint.txt','specification.md']})
artifacts=[]
exclude={'execution.json','evidence/run-check-final.txt','evidence/run-check-final-status.json'}
for p in sorted(out.rglob('*')):
 if not p.is_file() or str(p.relative_to(out)) in exclude: continue
 rel=str(p.relative_to(out));kind='source' if rel.startswith('sources/') or rel in ['evidence/input-inventory.json','evidence/run-metadata.json'] else 'presentation'
 desc={'path':rel,'sha256':sha(p),'kind':kind}
 if rel.startswith('evidence/phase-') and p.suffix=='.json':
  identity=json.loads(p.read_text())['qore_evidence']; desc.update({k:identity[k] for k in ['candidate_sha256','target_snapshot_sha256','observed_at']});desc['kind']='execution'
 artifacts.append(desc)
run={'schema':'qore-run/1','id':meta['run_id'],'method':'plan','skill':'qore-plan','candidate_sha256':meta['candidate_sha256'],'target':{'label':'Frozen prepared-input manifest; documentation target target/verification-protocol.md','snapshot_sha256':meta['target_snapshot_sha256']},'last_relevant_change':meta['last_relevant_change'],'environment':meta['environment'],'profile':None,'required_phases':['product','architecture','ux','delivery','qa','adjudication','spec_validation'],'phases':phases,'artifacts':artifacts,'commands':json.loads((out/'evidence/commands.json').read_text()),'limitations':[
 'No website/browser/network observation performed or required for this documentation-only plan. Runtime conformance, guard implementation and deployment identity remain unexamined.',
 'Candidate and enclosing prepared-input snapshot digests supplied by user; per-file inventories retained, but enclosing manifest serialization unavailable for independent recomputation.',
 'Exact first-wave dispatch instants unavailable; observed UTC enclosing intervals retained. Subsequent dispatch times are adjacent lead clock observations; exact host enqueue instants unavailable.',
 'Host retired Product and UX initial contexts when later roles were spawned. Fresh successor contexts performed their required cross-examination using all reports after barrier; initial reports were preserved.',
 'Actual token/billed agent-second counters unavailable from host tools. Roster records elapsed occupancy bounds; no zero usage asserted.',
 'QA and UX cross-examinations finished5 and15 seconds beyond role deadlines. Lead requested available reports at first cross deadline, but missed exact UX expiry request during drafting; full available report retained with monitoring gap disclosed.',
 'Role-local commands are recorded as workers reported them in complete reports; root cannot retrieve retired-context raw tool transcripts.',
 'Structural validators establish declared structure and evidence identity only, not reasoning correctness or approval to implement.',
 'No profile supplied or consumed. No application, shared-data, input or skill-resource mutation performed.'
 ],'coverage':'COMPLETE'}
(out/'execution.json').write_text(json.dumps(run,indent=2))
print(json.dumps({'execution_written':str(out/'execution.json'),'phases':len(phases),'artifacts':len(artifacts)}))
