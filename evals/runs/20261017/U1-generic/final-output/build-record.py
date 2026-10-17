import pathlib,json,hashlib,datetime,subprocess
out=pathlib.Path('/workspace/output');src=pathlib.Path('/workspace/worker'); skill=src/'.agents/skills/qore-ux-review'
C='8b26119f383a7d5853c1bd2ab5f678e08966300846c0d6f2784351c1f5a59e8d';T='ca02b75180a201ba8f9abb4e095a3d72cd0066f939e66c2e34bc7a781ad0c34d'
def read(n):return json.loads((out/n).read_text())
def save(n,x):(out/n).write_text(json.dumps(x,indent=2)+'\n')
b=read('budget-record.json');stamp=datetime.datetime.now(datetime.timezone.utc);b['recorded_at']=stamp.isoformat();b['wall_elapsed_seconds']=(stamp-datetime.datetime.fromisoformat(b['start_utc'])).total_seconds();save('budget-record.json',b)
phases=['scope','browser','state_transition','freshness','verdict']
run={'schema':'qore-run/1','id':'qore003-20261017-u1-generic-1','method':'ux','skill':'qore-ux-review','candidate_sha256':C,'target':{'label':'Entire frozen prepared-input manifest; declared public Back journey https://qaizen.io/labs -> readiness-check','snapshot_sha256':T},'last_relevant_change':'2026-10-17T09:53:58.681100+00:00','environment':{'id':'qore-qualification-qore003-20261017-u1-generic-1','operator':'agent','host':'Docker Desktop Linux arm64 / Codex0.162.0'},'profile':None,'scope':{'depth':'entry','supplemental_depth':'state','state_transition_applicable':True,'declaration':'scope-plan.json'},'required_phases':phases,'phases':[{'id':p,'actor_id':'/root','status':'PASS','artifacts':[p+'-phase.json']} for p in phases],'artifacts':[],'commands':read('command-records.json'),'limitations':read('limitations.json'),'coverage':'COMPLETE','observation_coverage':'COMPLETE','scoped_verdict':'DO-NOT-SHIP','roster':'roster.json','budget':'budget-record.json','skill_revision':{'version':'0.2.1','manifest':'input-manifest.json','source_release':'.agents/skills/qore-ux-review/references/release.json'},'validation_note':'PASS phase denotes completed method work, including establishing defects. Structural validator does not certify factual conclusions.'}
def collect():
 entries=[]
 for p in sorted(out.rglob('*')):
  if not p.is_file() or any(part.startswith('.') for part in p.relative_to(out).parts):continue
  name=str(p.relative_to(out))
  if name in ['execution.json','run-check-final.json','build-record.py']:continue
  item={'path':name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'kind':'presentation' if p.suffix=='.md' else 'source'}
  if name in [x+'-phase.json' for x in phases]:
   ident=read(name)['qore_evidence']; item.update({'kind':'execution',**{k:ident[k] for k in ('candidate_sha256','target_snapshot_sha256','observed_at')}})
  entries.append(item)
 return entries
run['artifacts']=collect();save('execution.json',run)
argv=['python3','-B',str(skill/'scripts/run-check.py'),str(out/'execution.json'),'--evidence-root',str(out)]
p=subprocess.run(argv,capture_output=True,text=True);save('run-check-initial.json',{'argv':argv,'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'observed_at':datetime.datetime.now(datetime.timezone.utc).isoformat()});print('Initial structural check',p.returncode,p.stdout,p.stderr)
if p.returncode: raise SystemExit(p.returncode)
# Retain this actual check as a declared command artifact, then validate the final record.
run['commands'].append({'argv':argv,'exit_code':p.returncode,'artifact':'run-check-initial.json'});run['artifacts']=collect();save('execution.json',run)
p=subprocess.run(argv,capture_output=True,text=True);save('run-check-final.json',{'argv':argv,'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'observed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reason_for_final_pass':'Check final record after adding the actual initial validator command/output to its artifact manifest. This output is a companion, avoiding a self-referential digest.'});print('Final structural check',p.returncode,p.stdout,p.stderr)
raise SystemExit(p.returncode)
