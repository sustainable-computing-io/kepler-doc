#!/usr/bin/env bash
# Commit root files to gh-pages that mike does not manage, and remove leftovers
# from the unversioned site that would shadow the 404 redirects.
#
# Usage: hack/gh-pages/tidy-root.sh   (run after mike deploy, before pushing gh-pages)

set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
WORKTREE="$(mktemp -d)"
trap 'git worktree remove --force "$WORKTREE"' EXIT

git worktree add --quiet "$WORKTREE" gh-pages
cd "$WORKTREE"

# Keep version directories and aliases listed in versions.json, plus mike's root files.
keep="$(python3 -c '
import json
versions = json.load(open("versions.json"))
names = {v["version"] for v in versions} | {a for v in versions for a in v["aliases"]}
print("\n".join(sorted(names | {"versions.json", "index.html", "404.html", "CNAME", ".nojekyll", ".git"})))
')"

for entry in * .[!.]*; do
	[[ -e "$entry" ]] || continue
	if ! grep -qxF "$entry" <<<"$keep"; then
		git rm -r --quiet "$entry"
	fi
done

cp "$HERE/404.html" 404.html
echo "sustainable-computing.io" >CNAME
touch .nojekyll
git add 404.html CNAME .nojekyll

if git diff --cached --quiet; then
	echo "gh-pages root is tidy"
else
	git commit --quiet -m "chore: tidy gh-pages root"
	echo "Committed gh-pages root changes"
fi
