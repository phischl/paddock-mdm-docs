# Paddock website and documentation

The source of <https://phischl.github.io/paddock-mdm-docs/>: the landing page and the documentation of
[Paddock](https://github.com/phischl/paddock-mdm), open-source management for Linux workstations.

## Single source of truth

The documentation is written in the main repository and is **not** copied into this one. `scripts/sync-docs.sh`
takes it from `phischl/paddock-mdm` at a ref (default `main`) at build time:

| Source in `phischl/paddock-mdm` | On the site |
| --- | --- |
| `docs/operations/**` | Operations guide |
| `docs/compliance/**` | Compliance |
| `docs/architecture.md`, `docs/adr/**` | Architecture |
| `docs/assets/**` | logos and screenshots |
| `CHANGELOG.md` | Changelog (`docs/changelog.md`) |

`docs/plans`, `docs/poc` and `docs/reqirements` are never copied. Relative links that point outside the copied set
(source code, plans, the README) are rewritten to `https://github.com/phischl/paddock-mdm/blob/<ref>/…` by
`scripts/rewrite_links.py`; links to paths that do not exist in the main repository are reported. The copied files
are gitignored. Fix documentation in the main repository, never here.

This repository holds only the site itself: `mkdocs.yml` (theme and navigation), `docs/index.md` (landing page),
`docs/getting-started.md`, `docs/stylesheets/extra.css` (brand colours from the logo, contrast fixes) and
`docs/javascripts/a11y.js` (gives the theme's search dialog an accessible name).

A new document in the main repository needs an entry in the `nav` of `mkdocs.yml`: the strict build fails on a
document that is not in the navigation, so nothing is silently missing from the site.

## Local preview

Requires Python 3 and git. Check out `phischl/paddock-mdm` next to this repository, then:

```sh
pip install -r requirements.txt && scripts/sync-docs.sh ../paddock-mdm && mkdocs serve
```

Without an argument `scripts/sync-docs.sh` fetches the main repository from GitHub. `PADDOCK_REF=<branch|tag|commit>`
selects another ref. Before pushing, run `mkdocs build --strict`.

## Tooling

[MkDocs](https://www.mkdocs.org/) with [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/), both
pinned to exact versions in `requirements.txt`. They are used only in CI and for the local preview. Nothing else is
needed; the link rewriting uses only the Python standard library.

## Deployment

`.github/workflows/pages.yml` syncs the documentation, runs `mkdocs build --strict` and deploys the site to GitHub
Pages on every push to `main`, nightly, and on demand (`workflow_dispatch` with an optional ref of the main
repository). The repository's Pages source must be set to *GitHub Actions*.

## License

[MIT](LICENSE). The documentation itself is part of `phischl/paddock-mdm` and licensed there.
