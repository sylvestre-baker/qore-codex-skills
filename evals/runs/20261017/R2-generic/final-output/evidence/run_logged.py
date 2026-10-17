import subprocess,pathlib,json,datetime,sys
name=sys.argv[1]; cwd=sys.argv[2]; argv=sys.argv[3:]
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
start=now(); result=subprocess.run(argv,cwd=cwd,capture_output=True,text=True)
record={'argv':argv,'cwd':cwd,'started_at':start,'completed_at':now(),'exit_code':result.returncode,'stdout':result.stdout,'stderr':result.stderr}
pathlib.Path('/workspace/output/evidence/'+name+'.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
sys.exit(result.returncode)
