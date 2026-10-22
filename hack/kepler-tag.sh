#!/usr/bin/env bash
# Print the release tag the `kepler` submodule is pinned to.
# Shallow CI checkouts have no tags, so look the commit up on the remote.

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
sha="$(git -C "$ROOT/kepler" rev-parse HEAD)"
tag="$(git -C "$ROOT/kepler" ls-remote --tags origin 'v*' |
	awk -v sha="$sha" '$1 == sha { sub("refs/tags/", "", $2); sub(/\^\{\}$/, "", $2); print $2 }' |
	sort -uV | tail -n 1)"
if [[ ! "$tag" =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
	echo "error: kepler submodule at $sha is not a release tag" >&2
	exit 1
fi
echo "$tag"
