#!/bin/sh
set -eu

remote="${1:?remote url required}"
message="${2:-snapshot}"
branch="$(git symbolic-ref --short HEAD 2>/dev/null || printf 'main')"

if git remote get-url origin >/dev/null 2>&1; then
  git remote set-url origin "$remote"
else
  git remote add origin "$remote"
fi

log="$(mktemp /data/workspace/.push.XXXXXX)"
trap 'rm -f "$log"' EXIT

if [ -n "${KCU_PAT:-}" ]; then
  auth="$(printf 'x-access-token:%s' "$KCU_PAT" | base64 | tr -d '\n')"
  GIT_TERMINAL_PROMPT=0 git -c "http.extraHeader=Authorization: Basic $auth" push -u origin "$branch" >"$log" 2>&1 || true
else
  GIT_TERMINAL_PROMPT=0 git push -u origin "$branch" >"$log" 2>&1 || true
fi

if grep -qE '^(Everything up-to-date|To https://|remote: )' "$log" 2>/dev/null && ! grep -qiE '(fatal|error|403|401)' "$log"; then
  echo "[KCU] remote push $branch OK detail=git_http"
  cat "$log"
else
  echo "[KCU] remote push $branch DEGRADE detail=api_snapshot_fallback"
  python3 "$(dirname "$0")/api_push.py" "$message"
fi
