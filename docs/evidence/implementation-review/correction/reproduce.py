import pathlib,json,hashlib,subprocess,datetime,os
E=pathlib.Path('/workspace/fix-verification'); C=E/'cases'; C.mkdir(exist_ok=True)
roots={'old':pathlib.Path('/workspace/implementation-target/qore-skills-0.1.0'),'fixed':pathlib.Path('/workspace/fix-target/qore-skills-0.1.0')}
logs=[]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x): p.write_text(json.dumps(x,indent=2)+'\n')
def run(tag,argv,cwd=None):
 p=subprocess.run([str(a) for a in argv],cwd=cwd,text=True,capture_output=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'},timeout=90)
 r={'tag':tag,'argv':[str(a) for a in argv],'cwd':str(cwd or E),'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr};logs.append(r)
 save(E/'commands.json',logs)
 try:return json.loads(p.stdout)
 except:return None
for label,root in roots.items():
 records=[{'path':str(p.relative_to(root)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(root.rglob('*')) if p.is_file()]
 save(E/(label+'-source-manifest.json'),{'root':str(root),'files':records,'identity_sha256':hashlib.sha256(json.dumps(records,sort_keys=True).encode()).hexdigest()})
 for f in ['manifest.json','skills/qore-plan/references/release.json','skills/qore-review/references/release.json','skills/qore-ux-review/references/release.json']:
  dest=E/'target-manifests'/label/f;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes((root/f).read_bytes())
 run(label+'-verify-raw',['python3','-B',root/'tools/qore.py','verify',root])
# stop controls and boundaries
stops={}
def loop(scores):return {'in_scope':['G1'],'iterations':[{'n':i+1,'scores':{'G1':v},'measured':['G1']} for i,v in enumerate(scores)]}
for n in [1,2,3,4,5,6,7]:
 stops['constant3-'+str(n)]=loop([3]*n);stops['zero-'+str(n)]=loop([0]*n)
stops['improving']=loop([0,1,2,3,4]);stops['sixth-pass']=loop([0,1,2,3,3,4]);stops['seventh-pass']=loop([0,1,2,3,3,3,4]);stops['pass']=loop([4])
for gate in ['G1','toString','constructor','__proto__','hasOwnProperty','UNKNOWN']:
 stops['missing-'+gate]={'in_scope':[gate],'iterations':[{'n':1,'scores':{},'measured':[]}]}
stops['unmeasured-score']={'in_scope':['G1'],'iterations':[{'n':1,'scores':{'G1':5},'measured':[]}]}
stops['stale']={'in_scope':['G1'],'iterations':[{'n':1,'scores':{'G1':5},'measured':['G1'],'fix_applied':True}]}
stops['remeasured']={'in_scope':['G1'],'iterations':[{'n':1,'scores':{'G1':5},'measured':['G1'],'fix_applied':True},{'n':2,'scores':{'G1':5},'measured':['G1']}]}
for name,data in stops.items():
 p=C/('stop-'+name+'.json');save(p,data)
 for label,root in roots.items():run(label+'-stop-'+name,['node',root/'skills/qore-ux-review/scripts/stop-rule.mjs',p])
# independent specification inputs
base='  Scenario: AC01 Test\n    Given input\n    When executed\n    Then output'
outline=base.replace('Scenario:','Scenario Outline:').replace('Given input','Given <input>')
specs={'real':base,'outline-missing':outline,'outline-header':outline+'\n    Examples:\n      | input |','outline-valid':outline+'\n    Examples:\n      | input |\n      | x |','outline-empty-value':outline+'\n    Examples:\n      | input |\n      | |','outline-mismatched-columns':outline+'\n    Examples:\n      | other |\n      | x |','outline-ragged':outline+'\n    Examples:\n      | input |\n      | x | y |'}
for marker in ['"""','```']:
 key='quote' if marker=='"""' else 'backtick'
 specs['docstring-'+key]='  Scenario: AC01 Test\n    Given input\n      '+marker+'\n      When literal\n      Then literal\n      '+marker
 specs['docstring-real-'+key]=base.replace('    When executed','      '+marker+'text/plain\n      Scenario: AC99 literal\n      Examples:\n      '+marker+'\n    When executed')
 specs['docstring-unclosed-'+key]=base+'\n      '+marker+'\n      literal'
for name,body in specs.items():
 p=C/('spec-'+name+'.md');p.write_text('<!-- qore-spec/1 -->\n~~~~gherkin\nFeature: Probe\n'+body+'\n~~~~\nCoverage: AC01 -> US1\n```mermaid\nsequenceDiagram\n A->>B: Check\n```\n')
 for label,root in roots.items():run(label+'-spec-'+name,['bash',root/'skills/qore-plan/scripts/spec-lint.sh',p,'--json'])
# every severity and proof controls
for sev in ['critical','high','medium','low','info']:
 for proof in [None,'','   ','Run node checker.mjs with case.json: actual accepted, expected rejected.']:
  name=sev+'-'+('missing' if proof is None else 'blank' if not proof else 'spaces' if proof.isspace() else 'proof')
  f={'id':'AC01','title':'Boundary probe','severity':sev,'verdict':'CONFIRMED','evidence':'checker.mjs:40'}
  if proof is not None:f['counterexample']=proof
  p=C/('finding-'+name+'.json');save(p,{'findings':[f]})
  for label,root in roots.items():run(label+'-finding-'+name,['node',root/'skills/qore-review/scripts/finding-lint.mjs',p,'--verifier=ran','--json'])
# actual maintained compact profile and noncompact control
identities=[]
for label,root in roots.items():
 for compact in [True,False]:
  name=label+('-compact' if compact else '-pretty');p=C/(name+'-profile.json')
  data=json.loads((root/'profiles/qore.json').read_text());p.write_text(json.dumps(data,separators=(',',':')) if compact else json.dumps(data,indent=2)+'\n')
  out=E/('derived-'+name)
  result=run(name+'-derive',['python3','-B',root/'tools/qore.py','derive','--profile',p,'--project-root',root,'--output',out])
  run(name+'-verify',['python3','-B',root/'tools/qore.py','verify',out])
  identity={'label':name,'input_sha256':sha(p),'derive_profile':result.get('profile') if result else None,'manifest_profile':json.loads((out/'manifest.json').read_text())['profile'],'skills':[]}
  for method in ['plan','review','ux-review']:
   skill=out/('qore-'+method+'-qore');bundled=skill/'references/project.json'
   check=run(name+'-check-'+method,['python3','-B',skill/'scripts/project-check.py',bundled,'--root',root,'--method','ux' if method=='ux-review' else method])
   identity['skills'].append({'method':method,'bundled_sha256':sha(bundled),'same_bytes':p.read_bytes()==bundled.read_bytes(),'release_profile':json.loads((skill/'references/release.json').read_text())['profile'],'checker_profile':check['profile'],'checker_coverage':check['coverage']})
  identities.append(identity)
save(E/'profile-identities.json',identities)
run('full-current-tests',['python3','-B','-m','unittest','discover','-s','tests','-v'],roots['fixed'])
print('Recorded',len(logs),'commands')
