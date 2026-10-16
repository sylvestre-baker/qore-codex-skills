import pathlib,re,json,hashlib,shutil,datetime,os,struct,importlib.util
root=pathlib.Path('/workspace/qore-skills-0.1.0')
print('UTC',datetime.datetime.now(datetime.timezone.utc).isoformat())
print('Session identity: primary agent /root (host-provided conversation role); no opaque chat/session ID exposed. Evidence process PID',os.getpid())
for t in ['rg','python3','node','ffprobe','ffmpeg','pandoc','cmark','chromium','playwright']:
 print('HOST_TOOL',t,shutil.which(t))
for t in ['markdown','markdown_it','mistune','PIL']:
 print('PYTHON_MODULE',t, bool(importlib.util.find_spec(t)))
paths=['README.md','docs/architecture.md','docs/profiles.md','docs/evidence/browser/README.md','docs/evidence/browser/qaizen-transcript.md']
for name in paths:
 p=root/name; text=p.read_text();print('\nDOCUMENT',name,'sha256',hashlib.sha256(p.read_bytes()).hexdigest())
 for n,line in enumerate(text.splitlines(),1):
  print(f'{name}:{n}: {line}')
  for dest in re.findall(r'\]\(([^)]+)\)',line):
   if '://' in dest:print('EXTERNAL_NOT_FETCHED',dest);continue
   f,sep,frag=dest.partition('#');q=p.parent/f if f else p
   print('LOCAL_LINK',dest,'exists',q.exists())
   if frag and q.exists() and q.suffix=='.md':
    heads=re.findall(r'^#+ (.+)$',q.read_text(),re.M)
    slugs=[re.sub(r'[^\w\- ]','',h.lower()).replace(' ','-') for h in heads]
    print('ANCHOR_SOURCE_CHECK',frag,frag in slugs)
prov=json.loads((root/'docs/evidence/browser/provenance.json').read_text())
for a in prov['public_artifacts']:
 p=root/'docs/evidence/browser'/a['public_file'];print('PROVENANCE_HASH',a['public_file'],hashlib.sha256(p.read_bytes()).hexdigest()==a['sha256'])
obs=json.loads((root/'docs/evidence/browser/observations.json').read_text())
print('OBSERVATION_TOP_FIELDS',list(obs));print('OBSERVATION_STATE_TYPE',type(obs['states']).__name__)
mat=json.loads((root/'docs/evidence/browser/capability-matrix.json').read_text())
def walk(v):
 if isinstance(v,dict):
  for k,x in v.items():
   if k=='evidence':
    for ref in ([x] if isinstance(x,str) else x):
     f,_,ptr=ref.partition('#');p=root/'docs/evidence/browser'/f
     if ptr:
      try:
       obj=json.loads(p.read_text())
       for part in ptr.lstrip('/').split('/'):
        obj=obj[int(part)] if isinstance(obj,list) else obj[part.replace('~1','/').replace('~0','~')]
       print('JSON_POINTER',ref,'RESOLVES')
      except (ValueError,KeyError,IndexError) as e:print('JSON_POINTER',ref,'FAIL',str(e))
   walk(x)
 elif isinstance(v,list):
  for x in v:walk(x)
walk(mat)
print('OBSERVATION_COUNTS', 'network',len(obs['events']['network']),'page_errors',len(obs['events']['page_errors']))
for name in ['qaizen-entry.png','qaizen-question.png','qaizen-returned.png']:
 data=(root/'docs/evidence/browser'/name).read_bytes();print('PNG_DIMENSIONS',name,struct.unpack('>II',data[16:24]))
for name in ['qaizen-demo.en.vtt','qaizen-transcript.md']:
 for n,line in enumerate((root/'docs/evidence/browser'/name).read_text().splitlines(),1):print(f'{name}:{n}: {line}')
inv=json.loads((root/'docs/command-inventory.json').read_text())
for x in inv['documents']:
 if x['path'] in paths:print('INVENTORY_DOCUMENT_HASH',x['path'],hashlib.sha256((root/x['path']).read_bytes()).hexdigest()==x['sha256'])
for x in inv['entries']:
 if x['location']['path']=='README.md':
  print('README_INVENTORY',x['id'],x['execution'])
  if x['kind']=='shell_recipe':print('README_COMMAND_TEXT_PRESENT',x['id'],x['text'] in (root/'README.md').read_text())
