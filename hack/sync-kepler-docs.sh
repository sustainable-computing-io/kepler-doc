#!/usr/bin/env bash
# Copy version-bound docs from the kepler repo into docs/.
#
# Usage: hack/sync-kepler-docs.sh [ref]
#   ref: branch (main), tag (v0.12.0), or minor version (v0.12 resolves to the highest v0.12.* tag)
#
# Env:
#   KEPLER_REPO  git URL to clone (default: upstream)
#   KEPLER_DIR   local kepler checkout to copy from instead of cloning; ref is used only for links

set -euo pipefail

REF="${1:-main}"
REPO="${KEPLER_REPO:-https://github.com/sustainable-computing-io/kepler.git}"
BLOB_URL="https://github.com/sustainable-computing-io/kepler/blob"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

# upstream path (relative to docs/user/) -> path in this repo
FILES=(
	"installation.md:docs/kepler/installation/guide.md"
	"helm-updates.md:docs/kepler/installation/helm-updates.md"
	"configuration.md:docs/kepler/usage/configuration.md"
	"metrics.md:docs/kepler/design/metrics.md"
)

resolve_ref() {
	local ref="$1"
	if [[ "$ref" =~ ^v[0-9]+\.[0-9]+$ ]]; then
		git ls-remote --tags --refs "$REPO" "$ref.*" |
			sed 's|.*refs/tags/||' |
			grep -E "^$ref\.[0-9]+$" |
			sort -V | tail -n 1
	else
		echo "$ref"
	fi
}

TAG="$(resolve_ref "$REF")"
if [[ -z "$TAG" ]]; then
	echo "error: no tag matches $REF" >&2
	exit 1
fi

if [[ -n "${KEPLER_DIR:-}" ]]; then
	SRC="$KEPLER_DIR"
else
	SRC="$(mktemp -d)"
	trap 'rm -rf "$SRC"' EXIT
	git -c advice.detachedHead=false clone --quiet --depth 1 --branch "$TAG" "$REPO" "$SRC"
fi

echo "Syncing kepler docs from $TAG"
for entry in "${FILES[@]}"; do
	from="${entry%%:*}"
	to="$ROOT/${entry#*:}"
	mkdir -p "$(dirname "$to")"
	{
		echo "<!-- Synced from kepler@$TAG:docs/user/$from by hack/sync-kepler-docs.sh. Edit upstream: $BLOB_URL/main/docs/user/$from -->"
		echo
		# Links relative to docs/user/ point into the kepler repo; make them absolute.
		sed -E \
			-e "s#\]\(\.\./\.\./#](${BLOB_URL}/${TAG}/#g" \
			-e "s#\]\(\.\./#](${BLOB_URL}/${TAG}/docs/#g" \
			-e "s#\]\(installation\.md#](guide.md#g" \
			-e "s#\]\(configuration\.md#](../usage/configuration.md#g" \
			-e "s#\]\(metrics\.md#](../design/metrics.md#g" \
			"$SRC/docs/user/$from"
	} >"$to"
	echo "  docs/user/$from -> ${entry#*:}"
done
