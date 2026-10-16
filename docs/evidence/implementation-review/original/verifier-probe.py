import json, pathlib, tempfile, subprocess, hashlib, datetime
root=pathlib.Path('/workspace/implementation-target/qore-skills-0.1.0'); evidence=pathlib.Path('/workspace/implementation-review/evidence'); tmp=pathlib.Path(tempfile.mkdtemp(prefix='qore-independent-verifier-')); results={}
def run(label,args):
 p=subprocess.run(args,cwd=root,text=True,capture_output=True); results[label]={'command':args,'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr}; return p

def put(name,data):
 p=tmp/name;p.write_text(json.dumps(data,indent=2));return str(p)
run('inherited',['node','skills/qore-ux-review/scripts/stop-rule.mjs',put('inherited.json',{'in_scope':['toString'],'iterations':[{'n':1,'scores':{},'measured':[]}]})])
run('ordinary-missing',['node','skills/qore-ux-review/scripts/stop-rule.mjs',put('missing.json',{'in_scope':['G1'],'iterations':[{'n':1,'scores':{},'measured':[]}]})])
run('plateau',['node','skills/qore-ux-review/scripts/stop-rule.mjs',put('plateau.json',{'in_scope':['G1'],'iterations':[{'n':n,'scores':{'G1':3},'measured':['G1']} for n in range(1,5)]})])
run('nonfailure-plateau',['node','skills/qore-ux-review/scripts/stop-rule.mjs',put('other-plateau.json',{'in_scope':['G1'],'iterations':[{'n':n,'scores':{},'measured':[]} for n in range(1,5)]})])
base='<!-- qore-spec/1 -->\n```gherkin\nFeature: Probe\n  Scenario: AC01 Literal argument\n    Given a message\n      """\n      When this is only literal text\n      Then this is only literal text\n      """\n```\nCoverage: AC01 -> US1\n```mermaid\nsequenceDiagram\n  A->>B: Run\n```\n'
p=tmp/'docstring.md';p.write_text(base);run('docstring',['node','skills/qore-plan/scripts/spec-lint.mjs',str(p),'--json'])
p=tmp/'no-steps.md';p.write_text(base.replace('      When','      LiteralWhen').replace('      Then','      LiteralThen'));run('no-steps-control',['node','skills/qore-plan/scripts/spec-lint.mjs',str(p),'--json'])
p=tmp/'outline.md';p.write_text(base.replace('Scenario:','Scenario Outline:').replace('    Given a message\n      """\n      When this is only literal text\n      Then this is only literal text\n      """','    Given a <message>\n    When run\n    Then done'));run('outline',['node','skills/qore-plan/scripts/spec-lint.mjs',str(p),'--json'])
f={'id':'probe','title':'Known defect','severity':'medium','evidence':'source.js:1','verdict':'CONFIRMED'}
run('medium-no-counterexample',['node','skills/qore-review/scripts/finding-lint.mjs',put('medium.json',{'findings':[f]}),'--verifier=ran','--json'])
f['severity']='high';run('high-control',['node','skills/qore-review/scripts/finding-lint.mjs',put('high.json',{'findings':[f]}),'--verifier=ran','--json'])
profile=json.loads((root/'profiles/qore.json').read_text());p=tmp/'compact.json';p.write_text(json.dumps(profile,separators=(',',':')));dest=tmp/'derived'
run('derive',['python3','tools/qore.py','derive','--profile',str(p),'--project-root',str(root),'--output',str(dest)])
run('verify',['python3','tools/qore.py','verify',str(dest)])
bundled=dest/'qore-review-qore/references/project.json';run('project-check',['python3',str(dest/'qore-review-qore/scripts/project-check.py'),str(bundled),'--root',str(root),'--method','review'])
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
results['profile-hashes']={'input':h(p),'bundled':h(bundled),'manifest':json.loads((dest/'manifest.json').read_text())['profile'],'parsed_equal':json.loads(p.read_text())==json.loads(bundled.read_text())}
results['temp_root']=str(tmp);results['time']=datetime.datetime.now(datetime.timezone.utc).isoformat();(evidence/'verifier-results.json').write_text(json.dumps(results,indent=2));print(json.dumps(results,indent=2))
