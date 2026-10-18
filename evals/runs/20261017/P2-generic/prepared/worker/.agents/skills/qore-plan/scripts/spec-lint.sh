#!/usr/bin/env bash
# Keep the shell entry point independent of the caller's working directory.
set -eu
exec node "$(cd "$(dirname "$0")" && pwd)/spec-lint.mjs" "$@"
