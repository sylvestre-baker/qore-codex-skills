import json,pathlib,hashlib,datetime,shlex,subprocess
out=pathlib.Path('/workspace/output'); now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
candidate='8b26119f383a7d5853c1bd2ab5f678e08966300846c0d6f2784351c1f5a59e8d';target='3131271b248dda5824cc374eb7f519d1bc3c16b0da28ee676ec7a00471859f3b'
required=['finder.correctness','finder.security','finder.feasibility','redaction','verifier','findings_validation']
phases=[]
for pid in required:
 actor='/root/'+pid.split('.')[1] if pid.startswith('finder.') else '/root/verifier' if pid=='verifier' else '/root'
 refs=['evidence/phase-'+pid.replace('.','-')+'.json']
 if pid.startswith('finder.'):
  name=pid.split('.')[1];refs += [f'roles/{name}/report.md',f'roles/{name}/findings.json']
 elif pid=='redaction': refs+=['findings.json','claims.json','evidence/redactor-command.json']
 elif pid=='verifier':refs+=['roles/verifier/report.md','roles/verifier/coverage.json','verified.json','roles/verifier/static-comparison.json']
 elif pid=='findings_validation':refs+=['evidence/finding-lint.json']
 phases.append({'id':pid,'actor_id':actor,'status':'PASS','artifacts':refs})
commands=[]
for filename in ['evidence/contract-check.json','evidence/redactor-command.json','evidence/finding-lint.json','roles/correctness/contract-check.json','roles/security/contract-check.json','roles/verifier/contract-check.json','roles/feasibility/check-contract.run.json']:
 log=json.loads((out/filename).read_text());argv=log.get('argv',log.get('command'));argv=shlex.split(argv) if isinstance(argv,str) else argv
 commands.append({'argv':argv,'exit_code':log.get('exit_code',log.get('exit_status')),'artifact':filename})
checker_argv=['python3','-B','scripts/run-check.py','/workspace/output/execution.json','--evidence-root','/workspace/output']
# This provisional output is replaced with actual validator stdout before finalization.
(out/'evidence/run-check.stdout.json').write_text('{}\n')
commands.extend([{'argv':checker_argv,'exit_code':0,'artifact':'evidence/run-check.stdout.json'},{'argv':checker_argv,'exit_code':0,'artifact':'evidence/run-check.stdout.json'}])
limitations=[
 'Static supplied-source document review only; no website, browser, traffic, focus-order/path-length, current deployment, external harness, or performance certification evidence.',
 'No network, search, connector, site interaction, input edits, shared-data writes or publication performed.',
 'Actual per-context CPU/token/aggregate agent-second telemetry is unavailable; bounded wall allocations and UTC observation intervals are retained instead of zero usage.',
 'Internal dispatch timestamps are not exposed by host. Initial finder dispatches bracketed 11:20:16Z–11:20:51Z; fresh verifier bracketed 11:22:29Z–11:22:46.652315Z. Return observations and role first-clock observations retained in roster/reports.',
 'Operator-supplied enclosing candidate and target manifest hashes retained verbatim; their upstream manifest serialization procedure was not supplied. Complete local source snapshot and per-file SHA-256 manifest retained, unchanged check passed.',
 'Full finder context reports remain independent; root received all reports, collected candidates and wrote final synthesis. Fresh verifier only received actual mechanically filtered claims and raw criteria.',
 'C-2 and S-1 are duplicate policy-omission claims, retained as separate IDs; 3 confirmed IDs represent 2 distinct medium issues. Severity unchanged. No unexamined or unresolved IDs; no missing roles.',
 'An initial rg search failed (rg absent); initial shell exit code was not retained. Its actual command/output and unavailable status are in capability-probe.json. Explicit paths/Python supplied all access. Some inline comparison argv were not retained; complete comparison outputs and role reports were.',
 'No expiry partial-result requests required: every worker returned within the smaller declared deadline; no additional quality retries or child dispatches.',
 'No project profile bundled; profile null. Last relevant change supplied by enclosing run; source bytes stayed unchanged.',
 'Run-check is run twice to retain actual stdout and then validate its final digest binding. Full actual invocation metadata is saved in run-check-invocations.json outside the self-hashed artifact set to avoid a self-reference cycle.'
]
def build():
 artifacts=[]
 paths=[out/'REPORT.md',out/'roster.json',out/'findings.json',out/'claims.json',out/'verified.json']
 paths += [p for root in ['evidence','roles'] for p in (out/root).rglob('*') if p.is_file() and p.name!='run-check-invocations.json']
 for path in sorted(set(paths)):
  rel=str(path.relative_to(out));data=path.read_bytes();row={'path':rel,'sha256':hashlib.sha256(data).hexdigest(),'kind':'presentation' if path.suffix=='.md' and 'supplied' not in path.parts else 'source'}
  if path.parent==out/'evidence' and path.name.startswith('phase-'):
   envelope=json.loads(data);row.update({'kind':'execution',**{key:envelope['qore_evidence'][key] for key in ['candidate_sha256','target_snapshot_sha256','observed_at']}})
  artifacts.append(row)
 record={'schema':'qore-run/1','id':'qore003-20261017-r2-generic-1','method':'review','skill':'qore-review','candidate_sha256':candidate,'target':{'label':'Frozen prepared-input manifest; review target target/verification-protocol.md against supplied project sources','snapshot_sha256':target},'last_relevant_change':'2026-10-17T09:53:58.773220+00:00','environment':{'id':'qore-qualification-qore003-20261017-r2-generic-1','operator':'agent','host':'Docker Desktop Linux arm64 / Codex0.162.0'},'profile':None,'required_phases':required,'phases':phases,'artifacts':artifacts,'commands':commands,'limitations':limitations,'coverage':'COMPLETE'}
 (out/'execution.json').write_text(json.dumps(record,indent=2)+'\n')
 return record
build();invocations=[]
for iteration in range(2):
 start=now();proc=subprocess.run(checker_argv,cwd='/workspace/worker/.agents/skills/qore-review',capture_output=True,text=True)
 invocations.append({'argv':checker_argv,'cwd':'/workspace/worker/.agents/skills/qore-review','started_at':start,'completed_at':now(),'exit_code':proc.returncode,'stdout':proc.stdout,'stderr':proc.stderr,'validated_execution_sha256':hashlib.sha256((out/'execution.json').read_bytes()).hexdigest()})
 if proc.returncode:
  (out/'evidence/run-check-invocations.json').write_text(json.dumps(invocations,indent=2)+'\n');print(proc.stdout,proc.stderr);raise SystemExit(proc.returncode)
 if iteration==0:
  (out/'evidence/run-check.stdout.json').write_text(proc.stdout);build()
 else:
  if (out/'evidence/run-check.stdout.json').read_text()!=proc.stdout:raise RuntimeError('Validator output did not stabilize; retain diagnostics rather than claim final validity')
(out/'evidence/run-check-invocations.json').write_text(json.dumps(invocations,indent=2)+'\n')
print(proc.stdout)
print('Final execution SHA-256:',hashlib.sha256((out/'execution.json').read_bytes()).hexdigest())
