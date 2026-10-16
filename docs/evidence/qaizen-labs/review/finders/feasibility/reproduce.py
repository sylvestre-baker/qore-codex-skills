"""Local finder reproductions only. No network, tokens, or services used."""
import sys,json,tempfile
from pathlib import Path
from unittest.mock import patch
sys.dont_write_bytecode=True
sys.path.insert(0,'/workspace/project/tools')
from coordination import initialize,consume,request_review,save_register
from task_gate import DELIVERY_KEYS
from agent_mail import Client,receive
criteria=dict(task_id='recovery',task_revision=1,objective='test',authorized_scope='local',criteria=['check'],required_check_ids=['c'],expected_results={'c':'PASS'})
r=initialize(criteria,'1',True,True)
common={k:r[k] for k in ('task_id','task_revision','criteria_sha256')}
ack=dict(id='2',body=dict(common,kind='production_ack',assignment_message_id='1'))
delivery=dict(id='3',body=dict(common,kind='delivery',artifact_revision='a1',artifact_sha256='a'*64,artifact_path='artifact.txt'))
r=consume(r,[ack,delivery])
req={k:r[k] for k in DELIVERY_KEYS}; req.update(review_request_id='req1',review_session_id='fresh1',review_run_id='run1',review_session_fresh=True)
r=request_review(r,req)
verdict=dict(id='4',body=dict(req,kind='review_verdict',verdict='FAIL'))
r=consume(r,[verdict])
corrected=dict(id='5',body=dict(delivery['body'],artifact_revision='a2',artifact_sha256='b'*64))
next_r=consume(r,[corrected])
print(json.dumps(dict(case='F-FEAS-01',after_fail=r['state'],after_corrected_delivery=next_r['state'],decision=next_r['decisions'][-1]),indent=2))
# Deterministic scheduler simulation: each completed ACK takes 25 seconds,
# below the assigned 30-second per-call timeout. No real waits or HTTP.
clock=[0.0]; calls=[]
class SlowCompletedACKs(Client):
 def __init__(self): self.timeout=30
 def call(self,name,args):
  calls.append(dict(name=name,timeout=self.timeout,at=clock[0]))
  if name=='fetch_inbox':
   clock[0]+=1
   return [dict(id=i,thread_id='recovery',ack_required=True,body_md='{}') for i in range(2,8)]
  clock[0]+=25
  return {}
with tempfile.TemporaryDirectory() as t:
 p=Path(t)/'task.md'; save_register(p,'```qore-task\n{}\n```\n',initialize(criteria,'1',True,True))
 with patch('agent_mail.time.monotonic',side_effect=lambda:clock[0]):
  result=receive(SlowCompletedACKs(),p,'project','pm','recovery',seconds=120)
 print(json.dumps(dict(case='F-FEAS-02',simulated_elapsed_seconds=clock[0],result=result,calls=calls),indent=2))
