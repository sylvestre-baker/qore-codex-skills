from pathlib import Path
import json
out=Path('/workspace/qualification/finders/correctness')
findings=[{
'id':'C01','title':'Failed or incomplete review has no supported recovery transition','severity':'medium',
'evidence':'tools/coordination.py:79 only receives deliveries in IN_PROGRESS/awaiting=delivery; :92-95 moves FAIL to CHANGES_REQUIRED and PARTIAL/BLOCKED to BLOCKED with awaiting=None; :107 only permits review requests in REVIEW_REQUIRED/awaiting=None. docs/coordination.md:71 promises corrected artifacts as a new delivery/request after failed review. Measured reproduction: python3 -B /workspace/qualification/finders/correctness/reproduce.py; saved reproduction.json C01.',
 'trigger':'A valid current review returns FAIL, PARTIAL or BLOCKED, followed by a corrected delivery or fresh review request under unchanged task criteria.',
 'consequence':'The corrected delivery is permanently recorded as REJECT/not awaiting delivery; requesting another review raises not ready for a fresh review request. The documented correction loop cannot progress using the exposed commands. Manual register editing or a newly assigned task revision is required although criteria did not change.',
 'reproduction':'Run the saved reproduce.py. Each of FAIL/PARTIAL/BLOCKED produces CHANGES_REQUIRED or BLOCKED, rejects delivery a2, and rejects fresh request q2. Replaying the rejected delivery ID is skipped because it is already processed.',
 'unresolved_condition':'Finder-local reproduction only; a fresh verifier has not examined this candidate. No finding about whether the website itself fails.'
},{
'id':'C02','title':'Wrong review session or run can apply a terminal failure verdict','severity':'medium',
'evidence':'tools/coordination.py:88 compares only REVIEW_KEYS, which omit session/run (tools/task_gate.py:12); :89-95 stores verdict and applies FAIL/PARTIAL/BLOCKED before checking those fields. tools/task_gate.py:102-104 checks session/run only in the later completion gate. docs/coordination.md:21 requires verdict/proofs to carry the same identity and :73 says stale verdicts cannot change current acceptance. Measured reproduction: saved reproduction.json C02.',
 'trigger':'A verdict has the current task/artifact/request identity but missing or different review_session_id/review_run_id, and declares FAIL (likewise PARTIAL/BLOCKED). This can be a malformed or mismatched cooperative message; no hostile actor assumption is required.',
 'consequence':'The coordinator accepts the wrong-session FAIL and moves to CHANGES_REQUIRED. A subsequent verdict from the actual current session/run is rejected as not awaiting review. The completion gate cannot protect this earlier terminal transition; the correct reviewer loses its active recovery path.',
 'reproduction':'Run saved reproduce.py: request q1 targets s1/run1; verdict 6 targets old-session/old-run with FAIL and is recorded RECEIVE_VERDICT, state CHANGES_REQUIRED; verdict 7 from s1/run1 is REJECT/not awaiting review.',
 'unresolved_condition':'Finder-local reproduction only; no fresh verifier ran. A correctly identified PASS still must pass task_gate checks, so this does not claim false DONE.'
}]
(out/'findings.json').write_text(json.dumps({'findings':findings},indent=2)+'\n')
pre=json.loads((out/'preflight.json').read_text()); profile=json.loads(pre['stdout'])
use={'profile':profile['profile'],'preflight_exit_code':pre['exit_code'],'selected_commands':profile['commands'],'selected_invariants':profile['invariants'],'surfaces':profile['surfaces'],'consumed':[]}
for fact in profile['commands']+profile['invariants']:
 source=next(s for s in profile['sources'] if s['id']==fact['source'])
 effect={'surface-contract':'Inspected checker before executing declared argv from example root; result valid=true is offline consistency only.','close-focus':'Compared Close Enter, separate summary focus assertion and details closed assertion in browser-actions with the probe consumers; actual browser behavior unobserved.','back-focus':'Traced traverse-focus Tab/Shift+Tab loop and recorded focus-step events, followed by separate Enter and h1 focus assertion; no browser proof claimed.','unanswered-scope':'Checked unanswered samples before and after Close/Back, request method guard, top-level origin guard and blocked mutation recording; sampled policy only, browser behavior unobserved.'}[fact['id']]
 use['consumed'].append({'fact_id':fact['id'],'source_id':fact['source'],'current_source_sha256':source['actual_sha256'],'effect':effect})
(out/'profile-use.json').write_text(json.dumps(use,indent=2)+'\n')
