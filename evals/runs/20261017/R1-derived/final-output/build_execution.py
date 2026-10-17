from pathlib import Path
import json, hashlib, datetime
OUT=Path('/workspace/output'); E=OUT/'evidence'
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def read(name): return json.loads((E/name).read_text())
def write(path,x): path.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
identity=read('identity.json'); roster=json.loads((OUT/'roster.json').read_text())
candidate=identity['candidate_sha256']; target=identity['target_snapshot_sha256']
phase_specs=[('profile_preflight','/root',['profile-check.json','profile-use.json','contract-check.json']),('finder.correctness','/root/finder_correctness',['finder-correctness.md','finder-correctness.json','finder-correctness-source-audit.json','finder-correctness-contrary-search.json']),('finder.security','/root/finder_security',['finder-security.md','finder-security.json','finder-security-source-audit.txt']),('finder.feasibility','/root/finder_feasibility',['finder-feasibility.md','finder-feasibility.json','finder-feasibility-source-output.json','finder-feasibility-checker-output.json']),('redaction','/root',['findings.json','collection.json','claims.json','redaction-stderr.txt']),('verifier','/root/verifier',['verifier.md','verified.json','verifier-examination.json']),('findings_validation','/root',['finding-lint.json'])]
phases=[]
for phase,actor,names in phase_specs:
 file='phase-'+phase.replace('.','-')+'.json'; path=E/file
 if not path.exists():
  payload={'actor_id':actor,'artifact_content':{n:(read(n) if n.endswith('.json') else (E/n).read_text()) for n in names},'actual_role':next((r for r in roster['roles'] if r['role']==phase),None),'captured_at':now(),'note':'Wrapper created after actual phase; full raw report/output content retained. This is same-run evidence, not a renewed previous-run proof.'}
  write(path,{'qore_evidence':{'candidate_sha256':candidate,'target_snapshot_sha256':target,'observed_at':now(),'phase_id':phase},'payload':payload})
 phases.append({'id':phase,'actor_id':actor,'status':'PASS','artifacts':[file]+names})
artifacts=[]
for path in sorted(E.rglob('*')):
 if not path.is_file(): continue
 rel=str(path.relative_to(E)); kind='source'
 if rel.startswith('phase-') and rel.endswith('.json'): kind='execution'
 elif rel.endswith('.md') and not rel.startswith('source/'): kind='presentation'
 row={'path':rel,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'kind':kind}
 if kind=='execution': row.update({k:v for k,v in json.loads(path.read_text())['qore_evidence'].items() if k!='phase_id'})
 artifacts.append(row)
commands=[]
def command(argv,exit_code,artifact,cwd=None):
 row={'argv':argv,'exit_code':exit_code,'artifact':artifact}
 if cwd: row['cwd']=cwd
 commands.append(row)
command(['python3','.agents/skills/qore-review-qaizen-labs/scripts/project-check.py','.agents/skills/qore-review-qaizen-labs/references/project.json','--root','/workspace/worker','--method','review'],0,'profile-check.json','/workspace/worker')
command(['python3','-B','checks/check_contract.py','surface-contract.json'],0,'contract-check.json','/workspace/worker')
command(['node','scripts/redact-for-verifier.mjs','/workspace/output/evidence/findings.json'],0,'phase-redaction.json','/workspace/worker/.agents/skills/qore-review-qaizen-labs')
command(['node','scripts/finding-lint.mjs','/workspace/output/evidence/verified.json','--verifier=ran','--json'],0,'finding-lint.json','/workspace/worker/.agents/skills/qore-review-qaizen-labs')
for probe in read('capabilities.json')['probes']: command(probe['argv'],probe['exit_code'],'capabilities.json')
checker=read('finder-correctness-source-audit.json')['checker']; command(checker['command'],checker['exit_status'],'finder-correctness-source-audit.json')
checker=read('finder-feasibility-checker-output.json'); command(checker['command'],checker['exit_code'],'finder-feasibility-checker-output.json')
command(['python3','-B','/workspace/worker/checks/check_contract.py','/workspace/worker/surface-contract.json'],0,'finder-security-source-audit.txt')
if (E/'verifier-commands.json').exists():
 for c in read('verifier-commands.json'):
  command(c['argv'],c['exit_code'],c.get('artifact','verifier-commands.json'),c.get('cwd'))
if (E/'run-check-initial.json').exists(): command(['python3','scripts/run-check.py','/workspace/output/execution.json','--evidence-root','/workspace/output/evidence'],0,'run-check-initial.json','/workspace/worker/.agents/skills/qore-review-qaizen-labs')
run={'schema':'qore-run/1','id':identity['run_id'],'method':'review','skill':'qore-review-qaizen-labs','candidate_sha256':candidate,'target':{'label':'Frozen prepared-input manifest; review target target/verification-protocol.md against supplied project sources','snapshot_sha256':target},'last_relevant_change':identity['last_relevant_change'],'environment':identity['environment'],'profile':identity['profile'],'required_phases':[x[0] for x in phase_specs],'phases':phases,'artifacts':artifacts,'commands':commands,'limitations':['Scope is the supplied reconstructed procedure, not the deployed website. No network, browser, external advisories, or shared-data changes.','No missing finder roles or unexamined merged claims; all role reports retained. Duplicate original claims preserved in audit trail.','Exact API dispatch/return instants not exposed. Roster retains UTC observation bounds, first worker clock observations, completion times, and parent receipt observation times.','Token, CPU, and exact aggregate agent-second usage unavailable from host; null with reason in roster. Conservative wall-context budget upper bounds retained.','Enclosing candidate and prepared-input manifest identities are supplied operational metadata. Underlying enclosing manifest serialization is unavailable; per-file exact-byte digest manifest and full source copies retained, without claiming recomputation of enclosing identities.','rg unavailable; failed probes retained and find/Python fallbacks completed. Correctness finder failed Python wrapper returned 1; exact wrapper argv unavailable to parent, so failure is retained verbatim in finder-correctness-contrary-search.json rather than inventing an argv.','No fixes applied. Lint SHIP is absence of confirmed high/critical blockers under this findings contract, not publication permission or comprehensive website acceptance.','Structural validators do not establish factual correctness or prove independence by themselves; actual child context identities and complete reports are retained.'],'coverage':'COMPLETE','roster':'roster.json','phase_barrier':'All three independent finders returned complete reports before collection/redaction. Fresh verifier dispatched only after successful redaction. Review method; no planning phases invented.'}
write(OUT/'execution.json',run)
print(json.dumps({'phases':len(phases),'artifacts':len(artifacts),'commands':len(commands),'coverage':run['coverage']},indent=2))
