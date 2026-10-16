#!/usr/bin/env bash
# Prepare and operate an independent Linux qualification container without host mounts.
set -euo pipefail

usage() {
  printf '%s\n' 'Usage: tools/clean_room.sh prepare NAME AUDIT_DIR | inspect NAME | stage NAME ZIP | run NAME PROMPT_FILE [MODEL] | cleanup NAME'
}

command_name=${1:-}
container_name=${2:-}
if [[ ! "$container_name" =~ ^qore-qualification-[a-zA-Z0-9_.-]+$ ]]; then
  usage >&2
  exit 2
fi

case "$command_name" in
  prepare)
    audit_dir=${3:?Supply a new audit directory}
    mkdir "$audit_dir"
    build_context="$audit_dir/build-context"
    mkdir "$build_context"
    cat > "$build_context/Dockerfile" <<'DOCKERFILE'
FROM node:22-alpine@sha256:c610fcdfb1d5b4740dd70c284ed3cb16bb857e0f7166196e36a5501df7a3aa32
RUN apk add --no-cache bash python3 git ca-certificates libstdc++ file \
 && npm install --global @openai/codex@0.162.0 \
 && npm cache clean --force \
 && codex --version \
 && mkdir -p /workspace /home/node/.codex \
 && chown -R node:node /workspace /home/node/.codex
USER node
WORKDIR /workspace
CMD ["sleep", "infinity"]
DOCKERFILE
    image_name="$container_name:codex-0.162.0"
    docker build --pull=false --progress=plain --tag "$image_name" "$build_context" > "$audit_dir/build.log" 2>&1
    docker run --detach --init --name "$container_name" --label io.qaizen.qore.qualification=20261015 --cap-drop ALL --security-opt no-new-privileges --pids-limit 512 --memory 4g --cpus 2 "$image_name" > "$audit_dir/container-id.txt"
    bash "$0" inspect "$container_name" > "$audit_dir/environment.json"
    python3 - "$container_name" "$image_name" "$audit_dir" <<'PY'
import json, pathlib, subprocess, sys
name, image, audit = sys.argv[1:]
image_id = subprocess.check_output(['docker','image','inspect',image,'--format','{{.Id}}'],text=True).strip()
container_id = pathlib.Path(audit,'container-id.txt').read_text().strip()
print(json.dumps({'schema':'qore-clean-room-setup/1','status':'PREPARED_NOT_ACTIVATED','container':name,'container_id':container_id,'image':image,'image_id':image_id,'environment_file':str(pathlib.Path(audit,'environment.json')),'build_log':str(pathlib.Path(audit,'build.log'))},indent=2))
PY
    ;;
  inspect)
    [[ "$(docker inspect "$container_name" --format '{{index .Config.Labels "io.qaizen.qore.qualification"}}')" == '20261015' ]] || { printf '%s\n' 'Container is not owned by this qualification helper.' >&2; exit 2; }
    docker inspect "$container_name" --format '{{json .HostConfig}}' | python3 -c 'import json,sys; c=json.load(sys.stdin); assert not c.get("Binds") and not c.get("Privileged") and "ALL" in c.get("CapDrop",[]) and "no-new-privileges" in c.get("SecurityOpt",[]), "Container isolation differs from the declared setup"'
    docker inspect "$container_name" --format '{{json .Mounts}}' | python3 -c 'import json,sys; assert json.load(sys.stdin)==[], "Qualification requires no mounts"'
    docker exec -i "$container_name" python3 - <<'PY'
import json, os, pathlib, platform, subprocess
def command(*args):
    return subprocess.check_output(args,text=True,stderr=subprocess.STDOUT).strip()
help_text=command('codex','exec','--help')
print(json.dumps({'schema':'qore-clean-room-environment/1','status':'PREPARED_NOT_ACTIVATED','os':platform.platform(),'architecture':platform.machine(),'uid':os.getuid(),'gid':os.getgid(),'working_directory':os.getcwd(),'runtimes':{'node':command('node','--version'),'npm':command('npm','--version'),'python':command('python3','--version'),'codex':command('codex','--version'),'git':command('git','--version')},'codex_flags':{flag:flag in help_text for flag in ['--ignore-user-config','--ignore-rules','--ephemeral','--json']},'isolation':{'mounts':[],'privileged':False,'cap_drop':['ALL'],'no_new_privileges':True,'author_home_present':pathlib.Path('/Users').exists(),'candidate_staged':pathlib.Path('/workspace/candidate.zip').exists()},'limits':['No authenticated Codex invocation has been performed by this inspection.','This environment is an independent Linux container; it is not an external human first-use trial.']},indent=2))
PY
    ;;
  stage)
    archive=${3:?Supply the candidate ZIP}
    [[ -f "$archive" ]] || { printf '%s\n' 'Candidate ZIP is missing.' >&2; exit 2; }
    bash "$0" inspect "$container_name" >/dev/null
    docker exec "$container_name" test ! -e /workspace/candidate.zip
    docker exec -i "$container_name" sh -c 'umask 077; cat > /workspace/candidate.zip' < "$archive"
    docker exec -i "$container_name" python3 - <<'PY'
from pathlib import Path, PurePosixPath
import hashlib,json,stat,subprocess,zipfile
archive=Path('/workspace/candidate.zip')
with zipfile.ZipFile(archive) as bundle:
    members=bundle.infolist()
    if not members or len(members)>20000 or sum(m.file_size for m in members)>1_000_000_000:
        raise ValueError('Archive is empty or exceeds qualification limits')
    seen=set(); roots=set()
    for member in members:
        name=member.filename; pure=PurePosixPath(name)
        mode=member.external_attr>>16
        if not name or '\\' in name or '\x00' in name or pure.is_absolute() or '..' in pure.parts or name.rstrip('/')!=pure.as_posix() or name in seen or stat.S_IFMT(mode) not in (0,stat.S_IFREG,stat.S_IFDIR):
            raise ValueError('Unsafe or duplicate archive entry: '+repr(name))
        seen.add(name);roots.add(pure.parts[0])
    if len(roots)!=1:
        raise ValueError('Candidate must contain one versioned top-level directory')
    root=next(iter(roots))
    if root!='qore-skills-0.2.0' or not {root+'/tools/qore.py',root+'/manifest.json',root+'/skills/qore-review/SKILL.md'}.issubset(seen):
        raise ValueError('Unexpected candidate archive structure')
    target=Path('/workspace')/root
    if target.exists():raise ValueError('Candidate destination exists; create a fresh container')
    bundle.extractall('/workspace')
verification=subprocess.check_output(['python3','tools/qore.py','verify',str(target)],cwd=target,text=True)
print(json.dumps({'schema':'qore-clean-room-stage/1','status':'STAGED_NOT_ACTIVATED','candidate_sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'candidate_root':str(target),'verification':json.loads(verification)},indent=2))
PY
    ;;
  run)
    prompt_file=${3:?Supply an explicit qualification prompt file}
    model_name=${4:-}
    [[ -f "$prompt_file" ]] || { printf '%s\n' 'Qualification prompt file is missing.' >&2; exit 2; }
    bash "$0" inspect "$container_name" >/dev/null
    model_args=()
    if [[ -n "$model_name" ]]; then model_args=(--model "$model_name"); fi
    docker exec "$container_name" test -f /home/node/.codex/auth.json
    docker exec "$container_name" test -f /workspace/qore-skills-0.2.0/manifest.json
    docker exec -i --workdir /workspace/qore-skills-0.2.0 "$container_name" codex --ask-for-approval never exec --ignore-user-config --ignore-rules --ephemeral --json --skip-git-repo-check --sandbox danger-full-access "${model_args[@]}" - < "$prompt_file"
    ;;
  cleanup)
    [[ "$(docker inspect "$container_name" --format '{{index .Config.Labels "io.qaizen.qore.qualification"}}')" == '20261015' ]] || { printf '%s\n' 'Container is not owned by this qualification helper.' >&2; exit 2; }
    docker rm --force "$container_name" >/dev/null
    printf '%s\n' 'Removed the named qualification container. Its image is retained.'
    ;;
  *) usage >&2; exit 2 ;;
esac
