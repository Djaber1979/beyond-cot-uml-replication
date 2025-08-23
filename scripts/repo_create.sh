#!/usr/bin/env bash
set -euo pipefail

# Requires: https://cli.github.com/ (gh) and authenticated session: gh auth login
REPO_NAME="beyond-cot-uml-replication"
VISIBILITY="public" # or private

if gh repo view "${REPO_NAME}" >/dev/null 2>&1; then
  echo "Repository ${REPO_NAME} already exists. Skipping creation."
else
  gh repo create "${REPO_NAME}" --${VISIBILITY} --source=. --remote=origin --push
fi

echo "Done. Remote set to: $(git remote get-url origin)"
