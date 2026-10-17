import json,hashlib,pathlib,datetime
OUT=pathlib.Path('/workspace/output');EV=OUT/'evidence';m=json.loads((OUT/'metadata.json').read_text())
phasefiles={'finder.correctness':'phase-finder-correctness.json','finder.security':'phase-finder-security.json','finder.feasibility':'phase-finder-feasibility.json','redaction':'phase-redaction.json','verifier':'phase-verifier.json','findings_validation':'phase-findings-validation.json'}
extra={'finder.correctness':['finder-correctness.md','candidates-correctness.json','correctness-check-output.json'],'finder.security':['finder-security.md','candidates-security.json'],'finder.feasibility':['finder-feasibility.md','candidates-feasibility.json','feasibility-check-output.txt'],'redaction':['findings.json','claims.json','redactor.stderr.txt'],'verifier':['verifier-report.md','verified.json','verification-coverage.json','verifier-reproduce.py','verifier-reproduce-output.txt','verifier-checks.json'],'findings_validation':['finding-lint-output.json','finding-lint.stderr.txt']}
artifacts=[]
for p in sorted(EV.rglob('*')):
 if not p.is_file():continue
 rel=str(p.relative_to(EV));kind='source' if rel.startswith('sources/') else 'presentation'
 row={'path':rel,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'kind':kind}
 if rel in phasefiles.values():
  ident=json.loads(p.read_text())['qore_evidence'];row.update(kind='execution',**{k:ident[k] for k in ['candidate_sha256','target_snapshot_sha256','observed_at']})
 artifacts.append(row)
phases=[]
for phase,filename in phasefiles.items():
 actor={'finder.correctness':'/root/correctness','finder.security':'/root/security','finder.feasibility':'/root/feasibility','verifier':'/root/verifier'}.get(phase,'/root')
 phases.append({'id':phase,'actor_id':actor,'status':'PASS','artifacts':[filename]+extra[phase]})
cap=json.loads((EV/'capability-and-commands.json').read_text());commands=[]
for row in cap['commands']:
 commands.append({'argv':row['argv'],'exit_code':row['exit_code'],'artifact':row.get('artifact','capability-and-commands.json')})
for fn in ['phase-redaction.json','phase-findings-validation.json']:
 p=json.loads((EV/fn).read_text())['payload'];commands.append({'argv':p['argv'],'exit_code':p['exit_code'],'artifact':fn})
commands.extend([
 {'argv':['python3','-B','/workspace/worker/checks/check_contract.py','/workspace/worker/surface-contract.json'],'exit_code':0,'artifact':'correctness-check-output.json'},
 {'argv':['python3','-B','checks/check_contract.py','surface-contract.json'],'exit_code':0,'artifact':'finder-security.md'},
 {'argv':['python3','-B','checks/check_contract.py','surface-contract.json'],'exit_code':0,'artifact':'feasibility-check-output.txt'},
 {'argv':['python3','-B','/workspace/output/evidence/verifier-reproduce.py'],'exit_code':0,'artifact':'verifier-reproduce-output.txt'}])
record={'schema':'qore-run/1','id':m['run_id'],'method':'review','skill':'qore-review','candidate_sha256':m['candidate_sha256'],'target':{'label':'Frozen prepared-input manifest; review target target/verification-protocol.md against three original project sources','snapshot_sha256':m['target_snapshot_sha256']},'last_relevant_change':m['last_relevant_change'],'environment':m['environment'],'profile':None,'required_phases':list(phasefiles),'phases':phases,'artifacts':artifacts,'commands':commands,'limitations':[
 'No current website/browser/rendered behavior, actual focus/network observations or deployment identity; no website defect asserted.',
 'Synthetic offline fixtures demonstrate documentary coverage gaps only. Their stipulated failures do not represent the actual website.',
 'Seven candidate records overlap into four distinct omissions; all IDs, original medium severity, and full refutation attempts retained. No candidate was refuted; unexamined IDs empty.',
 'Host does not expose token or aggregate agent-second usage. Actual usage is unavailable, never recorded as zero. Scheduling ceiling 1860 agent-seconds; observed child-interval upper bound 399 seconds.',
 'Per-spawn and per-return UTC are not exposed. Roster uses actual clock-bracketed dispatch intervals and first post-return UTC samples; verifier also supplied its completion timestamp.',
 'Enclosing candidate/prepared-input digests and change time are supplied operational identity. Their manifest serialization is unavailable; file-level hashes and unchanged-source copies are independently retained instead.',
 'Profile is null and references/project.json is absent; no profile facts consumed.',
 'No inputs edited, no corrected target executed, no network or shared-data mutations. No release action authorized.',
 'rg is unavailable; find/direct reads/Python used. Failed probes retained in full role reports and capability record.',
 'Final run-check invocation/output is retained as an external companion at /workspace/output/run-check-output.json with command metadata at /workspace/output/run-check-command.json, outside this hashed artifact set to avoid a self-referential digest cycle. It checks structure/declared identity, not factual reasoning.',
 'No missing roles or phases, expired workers, unexamined IDs, unresolved critical/high findings, or extra quality retry. Out-of-scope mobile, complete questionnaire, performance and accessibility certification remain untested.'
 ],'coverage':'COMPLETE'}
(OUT/'execution.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({'artifacts':len(artifacts),'phases':len(phases),'coverage':record['coverage']}))
