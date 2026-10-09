#!/usr/bin/env bash
# Copies the documentation of phischl/paddock-mdm into docs/ of this site.
#
# Usage: scripts/sync-docs.sh [SOURCE]
#
#   SOURCE       a local clone of phischl/paddock-mdm; omitted: the repository is fetched from GitHub
#   PADDOCK_REF  the branch, tag or commit to copy (default: main)
#   PADDOCK_REPO the repository to fetch when SOURCE is omitted
#                (default: https://github.com/phischl/paddock-mdm.git)
#
# The main repository is the single source of truth: the copied files are gitignored here and never edited. Relative
# links that point outside the copied set are rewritten to GitHub (scripts/rewrite_links.py).
set -euo pipefail

ref="${PADDOCK_REF:-main}"
repo_url="${PADDOCK_REPO:-https://github.com/phischl/paddock-mdm.git}"
site_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
dest="${site_root}/docs"

# Source paths copied into the site. docs/plans, docs/poc and docs/reqirements are never copied.
paths=(docs/operations docs/compliance docs/architecture.md docs/adr docs/assets CHANGELOG.md)
# Generated paths below docs/, removed before every sync. Keep in sync with .gitignore.
generated=(operations compliance architecture.md adr assets changelog.md)

work="$(mktemp -d)"
trap 'rm -rf "${work}"' EXIT

if [[ $# -ge 1 ]]; then
  src="$(cd "$1" && pwd)"
  commit="$(git -C "${src}" rev-parse --verify --quiet "${ref}^{commit}" \
    || git -C "${src}" rev-parse --verify --quiet "origin/${ref}^{commit}" \
    || { echo "sync-docs: ref '${ref}' not found in ${src}" >&2; exit 1; })"
else
  src="${work}/repo"
  git init --quiet "${src}"
  git -C "${src}" fetch --quiet --depth 1 "${repo_url}" "${ref}"
  commit="$(git -C "${src}" rev-parse FETCH_HEAD)"
fi

echo "sync-docs: copying ${ref} (${commit:0:12}) from ${src}"

mkdir -p "${work}/out"
git -C "${src}" archive --format=tar "${commit}" -- "${paths[@]}" | tar -x -C "${work}/out"
git -C "${src}" ls-tree -r --name-only "${commit}" > "${work}/tree.txt"

for p in "${generated[@]}"; do
  rm -rf "${dest:?}/${p}"
done
mkdir -p "${dest}"
cp -R "${work}/out/docs/." "${dest}/"
cp "${work}/out/CHANGELOG.md" "${dest}/changelog.md"

python3 "${site_root}/scripts/rewrite_links.py" --ref "${ref}" --tree "${work}/tree.txt" --dest "${dest}"
