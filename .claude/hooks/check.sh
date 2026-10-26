#!/usr/bin/env bash
# Claude Code PostToolUse hook: after Claude edits Python, format the file, then
# run ruff and pytest (the same checks as CI). On failure, exit 2 so the output
# goes back to Claude.
set -uo pipefail

file=$(jq -r '.tool_input.file_path // empty')
repo=$(cd "$(dirname "$0")/../.." && pwd)
case "$file" in
  "$repo"/*.py) ;;
  *) exit 0 ;;
esac

cd "$repo"
uv run --frozen ruff format -q "$file"
if ! out=$(uv run --frozen ruff check . 2>&1 && uv run --frozen pytest -q 2>&1); then
  echo "ruff/pytest failed after editing $file:" >&2
  echo "$out" | tail -40 >&2
  exit 2
fi
