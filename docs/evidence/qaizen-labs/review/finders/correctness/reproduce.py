import json, sys
sys.path.insert(0, '/workspace/project/tools')
from coordination import initialize, consume, request_review
from task_gate import TASK_KEYS, DELIVERY_KEYS
s = {'task_id':'task','task_revision':1,'objective':'local','authorized_scope':'local','criteria':['check'],'required_check_ids':['x'],'expected_results':{'x':'PASS'}}
r = initialize(s,'1',True,True)
c = {k:r[k] for k in TASK_KEYS}
r = consume(r,[{'id':2,'body':dict(c,kind='production_ack',assignment_message_id='1')},{'id':3,'body':dict(c,kind='delivery',artifact_revision='a1',artifact_sha256='a'*64,artifact_path='a.txt')}])
q = {k:r[k] for k in DELIVERY_KEYS}
q.update(review_request_id='q1',review_session_id='s1',review_run_id='run1',review_session_fresh=True)
r = request_review(r,q)
results = []
for verdict in ('FAIL','PARTIAL','BLOCKED'):
    failed = consume(r,[{'id':4,'body':dict(q,kind='review_verdict',verdict=verdict)}])
    corrected = consume(failed,[{'id':5,'body':dict(c,kind='delivery',artifact_revision='a2',artifact_sha256='b'*64,artifact_path='b.txt')}])
    try:
        request_review(failed,dict(q,review_request_id='q2',review_session_id='s2',review_run_id='run2'))
        request_result = 'accepted'
    except ValueError as e:
        request_result = str(e)
    results.append({'verdict':verdict,'state':failed['state'],'corrected_delivery':corrected['decisions'][-1],'fresh_request':request_result})
wrong = consume(r,[{'id':6,'body':dict(q,kind='review_verdict',verdict='FAIL',review_session_id='old-session',review_run_id='old-run')}])
late = consume(wrong,[{'id':7,'body':dict(q,kind='review_verdict',verdict='PASS')}])
print(json.dumps({'C01':results,'C02':{'wrong_session_state':wrong['state'],'wrong_session_decision':wrong['decisions'][-1],'current_pass_state':late['state'],'current_pass_decision':late['decisions'][-1]}},indent=2))
