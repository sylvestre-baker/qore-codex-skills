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
    docker exec "$container_name" sh -c 'test ! -e /workspace/candidate.zip && test ! -L /workspace/candidate.zip'
    docker exec -i "$container_name" sh -c 'umask 077; cat > /workspace/candidate.zip' < "$archive"
    stage_record=$(docker exec -i "$container_name" python3 - <<'STAGE_PY'
from pathlib import Path, PurePosixPath
import hashlib, json, re, stat, subprocess, zipfile


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('Duplicate JSON member: ' + key)
        result[key] = value
    return result


def stage_archive(archive, workspace):
    """Validate the complete inventory before extracting or executing candidate code."""
    with zipfile.ZipFile(archive) as bundle:
        members = bundle.infolist()
        if not members or len(members) > 20000 or sum(m.file_size for m in members) > 1_000_000_000:
            raise ValueError('Archive is empty or exceeds qualification limits')
        seen, files, roots = set(), {}, set()
        for member in members:
            name, mode = member.filename, member.external_attr >> 16
            pure = PurePosixPath(name)
            canonical = name.rstrip('/')
            if (not name or '\\' in name or '\x00' in name or pure.is_absolute()
                    or '..' in pure.parts or canonical != pure.as_posix() or canonical in seen
                    or stat.S_IFMT(mode) not in (0, stat.S_IFREG, stat.S_IFDIR)):
                raise ValueError('Unsafe or duplicate archive entry: ' + repr(name))
            seen.add(canonical)
            roots.add(pure.parts[0])
            if not member.is_dir():
                files[canonical] = member
        if len(roots) != 1:
            raise ValueError('Candidate must contain one versioned top-level directory')
        root = next(iter(roots))
        manifest_name = root + '/manifest.json'
        if manifest_name not in files:
            raise ValueError('Candidate release manifest is missing')
        manifest_bytes = bundle.read(files[manifest_name])
        manifest = json.loads(manifest_bytes, object_pairs_hook=unique_object)
        if (not isinstance(manifest, dict) or manifest.get('schema') != 'qore-release/1'
                or manifest.get('kind') != 'generic' or manifest.get('host') != 'codex'
                or manifest.get('redistribution') != 'MIT-first-party'):
            raise ValueError('Unsupported candidate release metadata')
        version = manifest.get('version')
        if (not isinstance(version, str)
                or not re.fullmatch(r'[0-9]+\.[0-9]+\.[0-9]+(?:[-+][A-Za-z0-9.-]+)?', version)
                or root not in ('qore-skills-' + version, 'qore-skills-' + version + '-skills')):
            raise ValueError('Archive root does not match its release version')
        records = manifest.get('resources')
        if not isinstance(records, list) or not records:
            raise ValueError('Candidate release inventory is missing')
        expected = {manifest_name}
        for record in records:
            if (not isinstance(record, dict) or record.get('origin') not in ('first-party', 'Qaizen-public-observation')
                    or record.get('license') != 'MIT'):
                raise ValueError('Unsupported candidate resource rights')
            relative = record.get('path')
            if (not isinstance(relative, str) or not relative or '\\' in relative
                    or PurePosixPath(relative).is_absolute() or '..' in PurePosixPath(relative).parts
                    or PurePosixPath(relative).as_posix() != relative):
                raise ValueError('Unsafe candidate resource path')
            name = root + '/' + relative
            if name in expected:
                raise ValueError('Duplicate candidate resource: ' + relative)
            expected.add(name)
            if name not in files or hashlib.sha256(bundle.read(files[name])).hexdigest() != record.get('sha256'):
                raise ValueError('Missing or altered candidate resource: ' + relative)
        required = {root + '/tools/qore.py', root + '/skills/qore-review/SKILL.md'}
        if expected != set(files) or not required.issubset(files):
            raise ValueError('Unexpected candidate archive structure or inventory')
        target = workspace / root
        if target.exists() or target.is_symlink():
            raise ValueError('Candidate destination exists; create a fresh container')
        bundle.extractall(workspace)
    return {
        'schema': 'qore-clean-room-stage/1', 'status': 'STAGED_NOT_ACTIVATED',
        'candidate_sha256': hashlib.sha256(archive.read_bytes()).hexdigest(),
        'candidate_root': str(target), 'version': version,
        'manifest_sha256': hashlib.sha256(manifest_bytes).hexdigest(),
    }


if __name__ == '__main__':
    record = stage_archive(Path('/workspace/candidate.zip'), Path('/workspace'))
    target = Path(record['candidate_root'])
    verification = subprocess.check_output(
        ['python3', 'tools/qore.py', 'verify', str(target)], cwd=target,
        text=True,
    )
    record['verification'] = json.loads(verification, object_pairs_hook=unique_object)
    if record['verification'].get('valid') is not True or record['verification'].get('version') != record['version']:
        raise ValueError('Candidate verification did not confirm its version')
    print(json.dumps(record, indent=2))
STAGE_PY
    )
    # Root creates only control metadata; candidate code always runs as the worker.
    docker exec -i --user root "$container_name" python3 -c '
from pathlib import Path
import json, sys
directory = Path("/var/lib/qore-qualification")
if directory.is_symlink():
    raise ValueError("Stage metadata directory cannot be a symlink")
directory.mkdir(mode=0o755, parents=True, exist_ok=True)
if directory.stat().st_uid != 0 or directory.stat().st_mode & 0o022:
    raise ValueError("Stage metadata directory is not protected")
metadata = directory / "stage.json"
record = json.load(sys.stdin)
with metadata.open("x", encoding="utf-8") as output:
    json.dump(record, output, indent=2)
    output.write("\n")
metadata.chmod(0o444)
print(json.dumps(record, indent=2))
' <<< "$stage_record"
    ;;
  run)
    prompt_file=${3:?Supply an explicit qualification prompt file}
    model_name=${4:-}
    [[ -f "$prompt_file" ]] || { printf '%s\n' 'Qualification prompt file is missing.' >&2; exit 2; }
    bash "$0" inspect "$container_name" >/dev/null
    model_args=()
    if [[ -n "$model_name" ]]; then model_args=(--model "$model_name"); fi
    candidate_root=$(docker exec -i --user root "$container_name" python3 - <<'IDENTITY_PY'
from pathlib import Path, PurePosixPath
import hashlib, json, re


def read_stage(metadata, workspace):
    if metadata.is_symlink() or metadata.parent.is_symlink():
        raise ValueError('Stage identity cannot be a symlink')
    for protected in (metadata.parent, metadata):
        if protected.stat().st_uid != 0 or protected.stat().st_mode & 0o022:
            raise ValueError('Stage identity is not protected from the worker')
    record = json.loads(metadata.read_text())
    allowed = {'schema', 'status', 'candidate_sha256', 'candidate_root', 'version', 'manifest_sha256', 'verification'}
    if (not isinstance(record, dict) or set(record) != allowed
            or record.get('schema') != 'qore-clean-room-stage/1'
            or record.get('status') != 'STAGED_NOT_ACTIVATED'):
        raise ValueError('Unsupported stage identity')
    version = record.get('version')
    if not isinstance(version, str) or not re.fullmatch(r'[0-9]+\.[0-9]+\.[0-9]+(?:[-+][A-Za-z0-9.-]+)?', version):
        raise ValueError('Unsupported staged version')
    target = Path(record['candidate_root'])
    if (target.parent != workspace or target.name not in ('qore-skills-' + version, 'qore-skills-' + version + '-skills')
            or target.is_symlink() or not target.is_dir()):
        raise ValueError('Staged root differs from its protected identity')
    for key in ('candidate_sha256', 'manifest_sha256'):
        if not isinstance(record[key], str) or not re.fullmatch(r'[a-f0-9]{64}', record[key]):
            raise ValueError('Invalid stage digest')
    manifest_path = target / 'manifest.json'
    if manifest_path.is_symlink() or hashlib.sha256(manifest_path.read_bytes()).hexdigest() != record['manifest_sha256']:
        raise ValueError('Staged manifest changed')
    manifest = json.loads(manifest_path.read_text())
    if manifest.get('schema') != 'qore-release/1' or manifest.get('version') != version:
        raise ValueError('Staged release identity changed')
    if (not isinstance(record['verification'], dict) or record['verification'].get('valid') is not True
            or record['verification'].get('version') != version):
        raise ValueError('Staged verification result is invalid')
    expected = {'manifest.json'}
    for resource in manifest['resources']:
        expected.add(resource['path'])
        path = target / resource['path']
        if (path.is_symlink() or not path.resolve().is_relative_to(target.resolve())
                or hashlib.sha256(path.read_bytes()).hexdigest() != resource['sha256']):
            raise ValueError('Staged resource changed: ' + resource['path'])
    actual = set()
    for path in target.rglob('*'):
        if path.is_symlink():
            raise ValueError('Staged tree contains a symlink')
        if path.is_file():
            actual.add(path.relative_to(target).as_posix())
    if expected != actual:
        raise ValueError('Staged inventory changed')
    return str(target)


if __name__ == '__main__':
    print(read_stage(Path('/var/lib/qore-qualification/stage.json'), Path('/workspace')))
IDENTITY_PY
    )
    # Fail before authentication/model work if the declared sandbox cannot start.
    docker exec --workdir "$candidate_root" "$container_name" codex sandbox \
      -c 'sandbox_mode="workspace-write"' -c 'sandbox_workspace_write.network_access=false' \
      -- python3 -c 'print("QORE_SANDBOX_READY")'
    docker exec "$container_name" test -f /home/node/.codex/auth.json
    docker exec -i --workdir "$candidate_root" "$container_name" codex --ask-for-approval never exec \
      --ignore-user-config --ignore-rules --ephemeral --json --skip-git-repo-check \
      --sandbox workspace-write -c 'sandbox_workspace_write.network_access=false' \
      -c 'web_search="disabled"' "${model_args[@]}" - < "$prompt_file"
    ;;
  cleanup)
    [[ "$(docker inspect "$container_name" --format '{{index .Config.Labels "io.qaizen.qore.qualification"}}')" == '20261015' ]] || { printf '%s\n' 'Container is not owned by this qualification helper.' >&2; exit 2; }
    docker rm --force "$container_name" >/dev/null
    printf '%s\n' 'Removed the named qualification container. Its image is retained.'
    ;;
  *) usage >&2; exit 2 ;;
esac
