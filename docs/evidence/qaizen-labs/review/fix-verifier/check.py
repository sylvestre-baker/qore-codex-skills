import sys,json,tempfile,hashlib,subprocess,os,urllib.request
from pathlib import Path
from copy import deepcopy
from unittest.mock import patch
sys.dont_write_bytecode=True
sys.path.insert(0,'/workspace/project/tools')
import coordination as c,agent_mail as a
from task_gate import TASK_KEYS,DELIVERY_KEYS,digest
DEST=Path('/workspace/qualification/fix-verifier'); ROOT=Path('/workspace/project')
files=['tools/coordination.py','tools/agent_mail.py','tests/test_coordination.py','tests/test_agent_mail.py','docs/coordination.md']
hashes={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in files}
checks=[]
def ok(name,details): checks.append({'name':name,'status':'PASS','details':details})
s={'task_id':'independent','task_revision':1,'objective':'verify correction','authorized_scope':'temporary','criteria':['unchanged'],'required_check_ids':['x'],'expected_results':{'x':'PASS'}}
r=c.initialize(s,'assignment',True,True); common={k:r[k] for k in TASK_KEYS}
r=c.consume(r,[{'id':'1','body':dict(common,kind='production_ack',assignment_message_id='assignment')},{'id':'2','body':dict(common,kind='delivery',artifact_revision='v1',artifact_sha256=digest(b'one'),artifact_path='a')}])
req={k:r[k] for k in DELIVERY_KEYS};req.update(review_request_id='q1',review_session_id='s1',review_run_id='r1',review_session_fresh=True)
r=c.request_review(r,req)
for verdict in ['FAIL','PARTIAL','BLOCKED']:
 failed=c.consume(r,[{'id':'3','body':dict(req,kind='review_verdict',verdict=verdict)}]);snapshot=deepcopy(failed)
 resumed=c.resume_production(failed)
 assert failed==snapshot and resumed['criteria_sha256']==r['criteria_sha256']
 assert resumed['review_history']==[{k:failed[k] for k in ('delivery','request','pending_verdict')}]
 assert resumed['processed_message_ids']==failed['processed_message_ids'] and resumed['decisions'][:-1]==failed['decisions']
 assert 'pending_verdict' not in resumed and 'request' not in resumed
 for change in ({},{'task_revision':2},{'artifact_revision':'v2','criteria_sha256':'0'*64}):
  b=dict(common,kind='delivery',artifact_revision='v1',artifact_sha256=digest(b'two'),artifact_path='a');b.update(change)
  assert c.consume(resumed,[{'id':'bad','body':b}])['decisions'][-1]['action']=='REJECT'
 corrected=c.consume(resumed,[{'id':'4','body':dict(common,kind='delivery',artifact_revision='v2',artifact_sha256=digest(b'two'),artifact_path='a')}])
 second={k:corrected[k] for k in DELIVERY_KEYS};second.update(review_request_id='q2',review_session_id='s2',review_run_id='r2',review_session_fresh=True)
 current=c.request_review(corrected,second)
 stale=c.consume(current,[{'id':'late','body':dict(req,kind='review_verdict',verdict='PASS')}])
 assert stale['awaiting']=='review_verdict' and 'pending_verdict' not in stale
 valid=c.consume(stale,[{'id':'5','body':dict(second,kind='review_verdict',verdict='PASS')}]);assert valid['pending_verdict']['message_id']=='5'
 ok('correction_'+verdict,'Explicit correction preserves criteria, decisions, processed IDs and complete prior review; refuses same revision/stale criteria; new delivery/request rejects old verdict then receives current PASS.')
for state in [c.initialize(s,'a'),r,dict(r,state='DONE'),dict(r,state='BLOCKED',awaiting=None)]:
 try:c.resume_production(state)
 except ValueError:pass
 else:raise AssertionError('invalid resume accepted')
ok('resume_refusals','Assigned, active review, DONE and BLOCKED without negative review refused.')
for field in ['review_session_id','review_run_id']:
 for verdict in ['PASS','FAIL','PARTIAL','BLOCKED']:
  bad=dict(req,kind='review_verdict',verdict=verdict);bad[field]='wrong'
  rejected=c.consume(r,[{'id':'wrong','body':bad}])
  assert rejected['state']==r['state'] and rejected['awaiting']==r['awaiting'] and rejected['next_action_owner']==r['next_action_owner'] and 'pending_verdict' not in rejected
  assert rejected['decisions'][-1]['action']=='REJECT'
  valid=c.consume(rejected,[{'id':'valid','body':dict(req,kind='review_verdict',verdict=verdict)}]);assert valid['pending_verdict']['verdict']==verdict
ok('identity_matrix','8 mismatches rejected without poisoning wait; all four matching verdicts subsequently accepted.')
class Stop(Exception):pass
captures=[]
class Dispatch(urllib.request.HTTPHandler):
 def http_open(self,request):
  captures.append({'host':request.host,'selector':request.selector,'bearer_present':request.get_header('Authorization')=='Bearer SYNTHETIC'})
  raise Stop()
build=urllib.request.build_opener
with patch.dict(os.environ,{'http_proxy':'http://synthetic.invalid:8888','HTTP_PROXY':'http://synthetic.invalid:8888','all_proxy':'http://synthetic.invalid:8888','no_proxy':''},clear=True),patch.object(urllib.request,'build_opener',lambda *h:build(*h,Dispatch())):
 try:a.Client('http://127.0.0.1:8765/mcp/','SYNTHETIC').call('fetch_inbox',{})
 except Stop:pass
assert captures==[{'host':'127.0.0.1:8765','selector':'/mcp/','bearer_present':True}]
for url,token in [('http://remote.invalid/','x'),('http://user:pass@localhost/','x'),('https://localhost/','x'),('http://localhost/','')]:
 try:a.Client(url,token)
 except ValueError:pass
 else:raise AssertionError('endpoint accepted')
try:a.NoRedirect().redirect_request(None,None,None,None,None,None)
except ValueError:pass
else:raise AssertionError('redirect accepted')
ok('proxy_and_refusals',{'dispatch':captures,'socket_opened':False,'refused':'remote, userinfo, HTTPS, missing token, redirect'})
clock=[0.];calls=[]
entries=[{'id':i,'thread_id':'independent','ack_required':True,'body_md':'{}'} for i in range(10,17)]
class Timed(a.Client):
 def __init__(self):self.timeout=30
 def call(self,name,args):
  calls.append({'name':name,'start':clock[0],'timeout':self.timeout,'id':args.get('message_id')})
  if name!='fetch_inbox':assert str(args['message_id']) in c.load_register(p)[1]['processed_message_ids']
  clock[0]+=min(2 if name=='fetch_inbox' else 20,self.timeout)
  return entries if name=='fetch_inbox' else {}
with tempfile.TemporaryDirectory() as t:
 p=Path(t)/'r.md';c.save_register(p,'notes\n```qore-task\n{}\n```',c.initialize(s,'assignment'))
 with patch.object(a.time,'monotonic',lambda:clock[0]): first=a.receive(Timed(),p,'local','PM','independent',120)
 assert clock[0]==120 and len(first['acknowledged'])==6
 assert all(x['start']<120 and 0<x['timeout']<=min(30,120-x['start']) for x in calls)
 before=c.load_register(p)[1];first_calls=deepcopy(calls);calls.clear();clock[0]=0
 with patch.object(a.time,'monotonic',lambda:clock[0]):second=a.receive(Timed(),p,'local','PM','independent',0)
 # Snapshot's shorter budget may replay earlier ACKs first. A subsequent fast transport proves last pending ACK is reachable.
 replay=[]
 class Fast:
  def call(self,name,args):
   if name=='fetch_inbox':return entries
   replay.append(args['message_id']);return {}
 a.receive(Fast(),p,'local','PM','independent',0)
 assert 16 in replay and c.load_register(p)[1]==before
ok('ack_deadline_and_durable_replay',{'first':first,'calls':first_calls,'replayed_ids':replay,'durable_register_unchanged_on_replay':True,'virtual_time_only':True})
suites=[]
for pattern in ['test_coordination.py','test_agent_mail.py','test_task_gate.py']:
 proc=subprocess.run([sys.executable,'-B','-m','unittest','discover','-s','tests','-p',pattern,'-v'],cwd=ROOT,capture_output=True,text=True)
 (DEST/(pattern+'.log')).write_text(proc.stdout+proc.stderr);assert proc.returncode==0
 suites.append({'pattern':pattern,'exit_code':proc.returncode,'log':pattern+'.log'})
assert hashes=={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in files}
original=json.loads(Path('/workspace/qualification/verifier/verified.json').read_text())
results={'scope':files,'sha256':hashes,'checks':checks,'suites':suites,'findings':[{'id':f['id'],'title':f['title'],'severity':f['severity'],'original_verdict':f['verdict'],'current_status':'RESOLVED'} for f in original['findings']],'qualification':'Scheduling window only: synchronous HTTP socket timeout is not an absolute OS deadline against slow-drip bytes. No live network, services or credentials.','unfinished':[]}
(DEST/'results.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps({'checks':len(checks),'suites':len(suites),'findings':results['findings']},indent=2))
