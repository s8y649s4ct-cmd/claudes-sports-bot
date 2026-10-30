#!/usr/bin/env bash
# Commit & push Claude's Sports Bot to GitHub Pages if anything changed.
set -euo pipefail; cd "$(dirname "$0")"
python3 -c "import json;json.load(open('picks.json'))"
git add -A; git diff --cached --quiet && exit 0
git -c user.name="Claude's Sports Bot" -c user.email="csb@users.noreply.github.com" commit -qm "Refresh picks $(date '+%Y-%m-%d %H:%M %Z')"
git push -q origin main
