#!/usr/bin/env bash
# Publish the map: stamp meta.json (SAST now), commit all changes, push to GitHub Pages.
# Usage: scripts/publish.sh "Weekly 2026-10-05: add Erf 123 George"
set -euo pipefail
cd "$(dirname "$0")/.."
msg="${1:-Update $(TZ=Africa/Johannesburg date +%F)}"
if [ -z "$(git status --porcelain -- . ':!meta.json')" ]; then
  echo "Nothing changed; not stamping or committing."; exit 0
fi
python3 scripts/stamp_updated.py
git add -A
SKIP_STAMP=1 git commit -m "$msg"
git push origin HEAD:main
echo "Pushed. GitHub Pages usually rebuilds in 1-2 min: https://radient737.github.io/techtrust-dev-apps-map/meta.json"
