import sys,json,tempfile,io,os
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,'/workspace/project/tools')
import coordination as c, agent_mail as a
from task_gate import TASK_KEYS,DELIVERY_KEYS,digest
out={}
s={'task_id':'synthetic-73','task_revision':1,'objective':'check local bytes','authorized_scope':'temporary only','criteria':['current review'],'required_check_ids':['one'],'expected_results':{'one':'PASS'}}
r=c.initialize(s,'assign-73',True,True); common={k:r[k] for k in TASK_KEYS}
r=c.consume(r,[{'id':'2','body':dict(common,kind='production_ack',assignment_message_id='assign-73')},{'id':'3','body':dict(common,kind='delivery',artifact_revision='v1',artifact_sha256=digest(b'old'),artifact_path='artifact.txt')}])
req={k:r[k] for k in DELIVERY_KEYS}; req.update(review_request_id='request-73',review_session_id='fresh-73',review_run_id='run-73',review_session_fresh=True)
r=c.request_review(r,req)
for verdict in ['FAIL','PARTIAL','BLOCKED']:
 failed=c.consume(r,[{'id':'4','body':dict(req,kind='review_verdict',verdict=verdict)}])
 corrected=c.consume(failed,[{'id':'5','body':dict(common,kind='delivery',artifact_revision='v2',artifact_sha256=digest(b'corrected'),artifact_path='artifact.txt')}])
 try:c.request_review(corrected,dict(req,artifact_revision='v2')); error=None
 except ValueError as e:error=str(e)
 out['recovery_'+verdict]={'after_verdict':failed,'after_corrected_delivery':corrected,'request_error':error}
for field in ['review_session_id','review_run_id']:
 for verdict in ['FAIL','PARTIAL','BLOCKED']:
  body=dict(req,kind='review_verdict',verdict=verdict);body[field]='old-identity'
  changed=c.consume(r,[{'id':'wrong-'+field+verdict,'body':body}])
  out['mismatch_'+field+'_'+verdict]={'input':body,'before_state':r['state'],'after':changed}
# Stop immediately at HTTP dispatch: no socket is opened.
import urllib.request
class Capture(urllib.request.HTTPHandler):
 def http_open(self,request):
  out['proxy_dispatch']={'host':request.host,'selector':request.selector,'authorization':request.get_header('Authorization'),'type':request.type,'socket_opened':False}
  raise RuntimeError('STOP BEFORE SOCKET')
original=urllib.request.build_opener
def opener(*handlers):return original(*handlers,Capture())
with patch.dict(os.environ,{'http_proxy':'http://synthetic-proxy.invalid:8123','no_proxy':'','REQUEST_METHOD':''},clear=True),patch.object(urllib.request,'build_opener',opener):
 try:a.Client('http://127.0.0.1:8765/mcp/','SYNTHETIC-73').call('fetch_inbox',{})
 except RuntimeError:pass
# Virtual time, actual receive and durable register writes; not wire timing.
clock=[0.0];calls=[]
class Timed(a.Client):
 def __init__(self):super().__init__('http://127.0.0.1:8765/mcp/','SYNTHETIC')
 def call(self,name,args):
  calls.append({'name':name,'start':clock[0],'timeout':self.timeout})
  if name=='fetch_inbox':
   clock[0]+=2
   return [{'id':i,'thread_id':'synthetic-73','ack_required':True,'body_md':'{}'} for i in range(10,17)]
  clock[0]+=20
  return {}
with tempfile.TemporaryDirectory() as temp:
 p=Path(temp)/'register.md';c.save_register(p,'```qore-task\n{}\n```',c.initialize(s,'assign-73',True,True))
 with patch.object(a.time,'monotonic',lambda:clock[0]):result=a.receive(Timed(),p,'local','PM','synthetic-73',120)
 out['deadline']={'elapsed_simulated_seconds':clock[0],'calls':calls,'result':result,'socket_opened':False}
assert out['recovery_FAIL']['after_corrected_delivery']['decisions'][-1]['reason']=='not awaiting delivery'
assert out['mismatch_review_session_id_FAIL']['after']['state']=='CHANGES_REQUIRED'
assert out['proxy_dispatch']['host']=='synthetic-proxy.invalid:8123'
assert out['deadline']['elapsed_simulated_seconds']==142
print(json.dumps(out,indent=2))
