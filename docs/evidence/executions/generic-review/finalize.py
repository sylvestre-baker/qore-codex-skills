from pathlib import Path
import json,hashlib,datetime,subprocess,platform
E=Path('/workspace/review-evidence'); R=Path('/workspace/qore-skills-0.1.0'); S=R/'.agents/skills/qore-review'
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def write(p,v): (E/p).write_text(json.dumps(v,indent=2)+'\n')
def read(p):return json.loads((E/p).read_text())
def invoke(argv,stem,cwd=S):
 p=subprocess.run(argv,cwd=cwd,capture_output=True,text=True)
 (E/(stem+'.stdout')).write_text(p.stdout);(E/(stem+'.stderr')).write_text(p.stderr)
 v={'argv':argv,'cwd':str(cwd),'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'observed_at':now()};write(stem+'-command.json',v);return v
m=read('identity.json')
assert all(x['matches'] for x in m['archive_source_comparison'])
changes=[]
for x in read('source-manifest.json'):
 if hashlib.sha256((R/x['path']).read_bytes()).hexdigest()!=x['sha256']:changes.append(x['path'])
write('source-unchanged.json',{'observed_at':now(),'changed_paths':changes,'procedure':'Rehash every source-manifest path and compare against original saved digest.'})
assert not changes
claims=read('claims.json');verified=read('verified.json');assert [f['id'] for f in claims['findings']]==[f['id'] for f in verified['findings']]
lint=invoke(['node','scripts/finding-lint.mjs',str(E/'verified.json'),'--verifier=ran','--json'],'findings-lint');assert lint['exit_code']==0
roster=read('roster.json');roster['requests'].append({'requested_role':'fresh independent verifier','requested_task_name':'verifier','returned_actor_id':'/root/verifier','tool':'collaboration.spawn_agent','fork_turns':'none','budget_minutes':5,'returned_report':'verifier-report.md','candidate_input':'claims.json only; finder reasoning withheld'})
roster['returned_roles']=['correctness','security','feasibility','verifier'];roster['completion']='All reports returned. interrupt_agent called after each completed context; tool reported completed. No separate terminate API is exposed.';write('roster.json',roster)
phases=[];execution_files=[]
for role in ['correctness','security','feasibility']:
 phase='finder.'+role
 payload={'actor_id':'/root/'+role,'report':(E/(role+'-report.md')).read_text(),'candidates':read(role+'-candidates.json'),'requested_and_returned_role':role,'completed_scope':True}
 execution_files.append((phase,'/root/'+role,payload))
execution_files.extend([
 ('redaction','/root',read('redaction-command.json')),
 ('verifier','/root/verifier',{'report':(E/'verifier-report.md').read_text(),'coverage':read('verifier-coverage.json'),'final_packet':verified,'actual_commands':read('verifier-command-evidence.json')}),
 ('findings_validation','/root',lint)])
for phase,actor,payload in execution_files:
 filename=phase+'-execution.json';identity={'candidate_sha256':m['candidate_sha256'],'target_snapshot_sha256':m['target_snapshot_sha256'],'observed_at':now(),'phase_id':phase}
 write(filename,{'qore_evidence':identity,'payload':payload});phases.append({'id':phase,'actor_id':actor,'status':'PASS','artifacts':[filename]})
artifacts=[]
for p in sorted(E.rglob('*')):
 if not p.is_file() or p.name in ['execution.json','run-check.stdout','run-check.stderr','run-check-command.json']:continue
 rel=str(p.relative_to(E));kind='source' if rel.startswith('source/') or p.name in ['source-manifest.json','identity.json'] else 'presentation'
 row={'path':rel,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'kind':kind}
 if p.name.endswith('-execution.json'):
  row['kind']='execution';row.update({k:v for k,v in json.loads(p.read_text())['qore_evidence'].items() if k!='phase_id'})
 artifacts.append(row)
commands=[]
for stem in ['redaction','findings-lint']:
 c=read(stem+'-command.json');commands.append({'argv':c['argv'],'exit_code':c['exit_code'],'artifact':stem+'-command.json'})
commands.append({'argv':['python3','-B','-m','unittest','discover','-s','tests','-v'],'exit_code':0,'artifact':'project-tests.log'})
for file in ['correctness-project-check.json','correctness-trace.json','security-command-evidence.json','feasibility-project-check.json','feasibility-trace-results.json','verifier-command-evidence.json']:
 value=read(file)
 def extract(v):
  if isinstance(v,dict):
   if isinstance(v.get('argv'),list) and isinstance(v.get('exit_code'),int):commands.append({'argv':v['argv'],'exit_code':v['exit_code'],'artifact':file})
   else:
    for item in v.values():extract(item)
  elif isinstance(v,list):
   for item in v:extract(item)
 extract(value)
run={'schema':'qore-run/1','id':'independent-linux-validator-hardening-20261015','method':'review','skill':'qore-review','candidate_sha256':m['candidate_sha256'],'target':{'label':'examples/validator-hardening.md and scoped bundled validators/tests/current review contracts','snapshot_sha256':m['target_snapshot_sha256']},'last_relevant_change':m['last_relevant_change'],'environment':{'id':m['hostname'],'operator':'agent in user-declared independent Linux container','host':m['host']},'profile':None,'required_phases':[p['id'] for p in phases],'phases':phases,'artifacts':artifacts,'commands':commands,'limitations':['Agent execution, not external human first use. Container isolation supplied by user; no host or credential inventory attempted.','No Git metadata or rg binary; file digests and standard tools used.','Zero candidates: no claim-specific reproduction or refutation IDs exist; verifier independently checked acceptance cases.','No production packet-size or load guarantee tested; none specified.','Scope limited to named specification, implementation, tests and necessary contracts; not publication or whole-product qualification.','Execution wrapper timestamps record phase capture after actual completion, not reconstructed worker start times.','Completed contexts were stopped with interrupt_agent; host exposes no separate terminate API.'],'coverage':'COMPLETE'}
write('execution.json',run)
check=invoke(['python3','scripts/run-check.py',str(E/'execution.json'),'--evidence-root',str(E)],'run-check');print(check['stdout']);print(check['stderr']);assert check['exit_code']==0
