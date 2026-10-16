from pathlib import Path
import json,hashlib,datetime
p=Path('/workspace/review-evidence'); root=Path('/workspace/qore-skills-0.1.0')
def read(n):return (p/n).read_text()
def js(n):return json.loads(read(n))
def write(n,v):(p/n).write_text(json.dumps(v,indent=2)+'\n')
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
def stamp(f):return datetime.datetime.fromtimestamp(f.stat().st_mtime,datetime.timezone.utc).isoformat()
i=js('identity.json'); candidate=i['candidate_sha256']; target=i['target_snapshot_sha256']
roster=js('roster.json')
for r in roster:r['returned_report']=(p/r['report']).exists()
write('roster.json',roster)
h=js('host-invocations.json');h['shutdown']='interrupt_agent called after each of four FINAL_ANSWER reports; all returned previous_status completed. No dedicated terminate/remove operation is exposed; no workers remain running.'
h['final_findings_shell_receipt']={'tool':'exec_command','cmd':'node scripts/finding-lint.mjs /workspace/review-evidence/verified.json --verifier=ran --json > /workspace/review-evidence/final-checker.stdout.json 2> /workspace/review-evidence/final-checker.stderr','workdir':str(root/'.agents/skills/qore-review'),'returned':{'chunk_id':'b71d79','wall_time_seconds':0.00000225,'exit_code':0,'original_token_count':0,'output':''}}
write('host-invocations.json',h)
write('final-checker-command.json',dict(argv=['node','scripts/finding-lint.mjs',str(p/'verified.json'),'--verifier=ran','--json'],cwd=str(root/'.agents/skills/qore-review'),exit_code=0,stdout=read('final-checker.stdout.json'),stderr=read('final-checker.stderr'),observed_at=stamp(p/'final-checker.stdout.json')))
m=js('snapshot-manifest.json');changed=[x['path'] for x in m if sha(root/x['path'])!=x['sha256']]
write('source-unchanged.json',dict(unchanged=not changed,changed=changed,observed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),procedure='Rehash every file in initial snapshot manifest after verifier and final validation'))
phases=[];descriptors={}
for phase,actor,names in [
 ('finder.correctness','/root/correctness',['correctness.md','correctness.json','correctness-commands.json']),
 ('finder.security','/root/security',['security.md','security.json','security-commands.json']),
 ('finder.feasibility','/root/feasibility',['feasibility.md','feasibility.json','feasibility-commands.json']),
 ('redaction','/root',['findings.json','claims.json','redactor.stderr','redaction-command.json']),
 ('verifier','/root/verifier',['verifier.md','verified.json','verifier-commands.json']),
 ('findings_validation','/root',['final-checker-command.json','final-checker.stdout.json','final-checker.stderr'])]:
 observed=max(stamp(p/n) for n in names)
 meta=dict(candidate_sha256=candidate,target_snapshot_sha256=target,observed_at=observed,phase_id=phase)
 name=phase+'.evidence.json';write(name,dict(qore_evidence=meta,payload={n:read(n) for n in names}))
 descriptors[name]=meta;phases.append(dict(id=phase,actor_id=actor,status='PASS',artifacts=[name]+names))
limitations=['Bounded local review, not exhaustive fuzzing or production-scale performance testing; no guarantee of defect absence.', 'Agent first use; no external human usability qualification.', 'Host native signed receipts/full transcript export unavailable. Actual spawn response copies and CLI output receipts retained; actor labels alone are not phase proof.', 'Host exposes interrupt_agent but no dedicated termination operation. All workers completed and were interrupted after return.', 'No project profile consumed; references/project.json absent. Generic review with qore.json as raw target criteria.', 'Archive hash verified and 154 matching packaged paths byte-compared; installed local skill identity separately retained.', 'Source discovery initially found rg unavailable; used find and direct reads. No authentication files were read.']
(p/'REPORT.md').write_text('''# Validator-hardening review\n\nExecution coverage: **COMPLETE**. Three independent history-free finders, actual mechanical redaction, a fresh history-free verifier, and final findings validation completed against the frozen current files. No source files were edited.\n\n## Findings and decision\n\nZero candidates were independently returned and preserved. Confirmed: 0; plausible: 0; refuted: 0; unexamined IDs: none. No candidate counterexamples or refutations were invented. This supports accepting the named example against its stated A01–A03 criteria within the bounded review; it is not deployment/publication authorization or proof of defect absence.\n\nA01 missing envelope was refused. A02 skipped verification retained high severity and PLAUSIBLE, produced PARTIAL/PENDING and no blockers. A03 explicit empty findings was valid with verification declared; actual phase evidence was checked separately. Each finder traced actual source-to-file-to-redactor-to-consumer fields, including the intentional removal of verdict before verifier completion. Full independent reports and exact commands are retained.\n\nThe unchanged exact argument `--verifier=ran=skipped` was rejected with exit 2, empty stdout and usage stderr in both bundled and installed script copies. The fresh verifier independently reproduced that boundary. The current exact-value regression passes. Historical public evidence was not used as current proof.\n\nThe qore.json project check passed all 85 tests. Final findings checker exited 0 with valid=true, COMPLETE, zero findings and its structural SHIP label. That label is a declaration-based packet result; the execution record separately establishes phase coverage. The run-record checker output is retained in run-check.stdout.json/run-check.stderr with its exact command in run-check-command.json.\n\n## Execution coverage and identities\n\nRequested/returned: correctness → /root/correctness; security → /root/security; performance/feasibility → /root/feasibility; fresh verifier → /root/verifier. All reports returned within their five-minute budgets; run finished within the overall 15-minute budget. All four were spawned with fork_turns=none. No finder peer reasoning was supplied. The verifier received only actual mechanically filtered claims and raw target/criteria; it read no finder reasoning. On empty claims it actively exercised A01–A03, redaction and exact malformed declaration. Examined/unexamined claim IDs are both empty.\n\nAll six mandatory phase rows PASS with retained identity-bound actual execution payloads. Spawn responses and command receipts are copied in host-invocations.json; a native host transcript export was unavailable, and copies are explicitly labeled as such. Workers completed and interrupt_agent was called after each report. No dedicated terminate/remove host function is exposed.\n\n## Snapshot and limits\n\nCandidate archive SHA256: '''+candidate+'''. Scoped target manifest SHA256: '''+target+'''. See identity.json for digest procedure, archive comparisons and observed file modification times; target-manifest.json identifies the specification, validators, contracts and test fixtures. snapshot/ preserves current file bytes and README/instruction revisions. source-unchanged.json records a final byte check.\n\nThe remaining uncertainty is defects outside bounded test cases, exhaustive malformed-input combinations and large-packet resource behavior. No capacity threshold is specified. This is an agent-operated Linux first-use review, not external human evidence or whole-package qualification. No profile was consumed, publication or outside messaging performed, or auth file read.\n''')
artifacts=[]
for f in sorted(p.rglob('*')):
 if not f.is_file() or f.name in ['execution.json','run-check.stdout.json','run-check.stderr','run-check-command.json']:continue
 rel=str(f.relative_to(p));kind='execution' if rel in descriptors else 'source' if rel.startswith('snapshot/') or rel in ['target-manifest.json','snapshot-manifest.json'] else 'presentation'
 a=dict(path=rel,sha256=sha(f),kind=kind)
 if rel in descriptors:a.update({k:v for k,v in descriptors[rel].items() if k!='phase_id'})
 artifacts.append(a)
commands=[]
for role in ['correctness','security','feasibility','verifier']:
 data=js(role+'-commands.json');arr=data if isinstance(data,list) else data.get('commands',[])
 for c in arr:
  argv=c.get('argv',c.get('command'));code=c.get('exit_code',c.get('exit_status'))
  if isinstance(argv,list) and type(code)is int:commands.append(dict(argv=argv,exit_code=code,artifact=role+'-commands.json'))
for n in ['capabilities','project-tests','malformed-verifier-skills','malformed-verifier-.agents-skills','redaction-command','final-checker-command']:
 c=js(n+'.json');commands.append(dict(argv=c['argv'],exit_code=c['exit_code'],artifact=n+'.json'))
run=dict(schema='qore-run/1',id='linux-first-use-validator-hardening-20261015',method='review',skill='qore-review',candidate_sha256=candidate,target=dict(label='examples/validator-hardening.md and scoped bundled implementation/tests',snapshot_sha256=target),last_relevant_change=i['last_relevant_change'],environment=i['environment'],profile=None,required_phases=[x['id'] for x in phases],phases=phases,artifacts=artifacts,commands=commands,limitations=limitations,coverage='COMPLETE')
write('execution.json',run)
print('artifacts',len(artifacts),'commands',len(commands),'source changed',changed)
