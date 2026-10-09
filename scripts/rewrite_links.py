#!/usr/bin/env python3
"""Rewrites relative links in the copied documentation (called by scripts/sync-docs.sh).

A link to a file inside the copied set is pointed at that file's place on the site. A link to anything else in the
main repository (source code, docs/plans, the README) is rewritten to its GitHub URL at the synced ref. A link to a
path that does not exist in the main repository is rewritten the same way and reported, because it is broken in
the source document.
"""

import argparse
import posixpath
import re
import sys
from pathlib import Path

GITHUB = "https://github.com/phischl/paddock-mdm"

# Source path prefix -> site path prefix (relative to docs/ of this site). Keep in sync with sync-docs.sh.
MAPPING = [
    ("docs/operations/", "operations/"),
    ("docs/compliance/", "compliance/"),
    ("docs/adr/", "adr/"),
    ("docs/assets/", "assets/"),
    ("docs/architecture.md", "architecture.md"),
    ("CHANGELOG.md", "changelog.md"),
]

SCHEME = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")
# [text](target "title") and ![alt](target); the target may be wrapped in <>.
INLINE = re.compile(r"(\]\(\s*)(<[^>]*>|[^)\s]+)")
# [label]: target
REFDEF = re.compile(r"^(\s{0,3}\[[^\]]+\]:\s*)(<[^>]*>|\S+)")
# src="…" and href="…" in raw HTML
HTML = re.compile(r"""(\b(?:src|href|srcset)=")([^"]+)""")
FENCE = re.compile(r"^\s*(```|~~~)")
CODE_SPAN = re.compile(r"(`+)(.+?)\1")


def site_path(source):
    for src, dst in MAPPING:
        if source == src or (src.endswith("/") and source.startswith(src)):
            return dst + source[len(src):]
    return None


class Rewriter:
    def __init__(self, ref, tree):
        self.ref = ref
        self.files = set(tree)
        self.dirs = {posixpath.dirname(f) for f in tree}
        for d in list(self.dirs):
            while d:
                d = posixpath.dirname(d)
                self.dirs.add(d)
        self.rewritten = 0
        self.broken = []

    def target(self, source_file, site_file, raw):
        wrapped = raw.startswith("<") and raw.endswith(">")
        link = raw[1:-1] if wrapped else raw
        if not link or link.startswith(("#", "/")) or SCHEME.match(link):
            return raw
        path, sep, frag = link.partition("#")
        path, qsep, query = path.partition("?")
        resolved = posixpath.normpath(posixpath.join(posixpath.dirname(source_file), path))
        if resolved.startswith(".."):
            self.broken.append((source_file, link))
            return raw
        suffix = (qsep + query if qsep else "") + (sep + frag if sep else "")

        new = None
        if resolved in self.files and site_path(resolved):
            new = posixpath.relpath(site_path(resolved), posixpath.dirname(site_file) or ".")
        elif resolved in self.dirs:
            readme = resolved + "/README.md"
            if readme in self.files and site_path(readme):
                new = posixpath.relpath(site_path(readme), posixpath.dirname(site_file) or ".")
            else:
                new = f"{GITHUB}/tree/{self.ref}/{resolved}"
        else:
            if resolved not in self.files:
                self.broken.append((source_file, link))
            new = f"{GITHUB}/blob/{self.ref}/{resolved}"
        new += suffix
        if new != link:
            self.rewritten += 1
        return f"<{new}>" if wrapped else new

    def rewrite_text(self, source_file, site_file, line, pattern):
        def repl(m):
            return m.group(1) + self.target(source_file, site_file, m.group(2))

        return pattern.sub(repl, line)

    def rewrite_line(self, source_file, site_file, line):
        # Leave code spans untouched: only rewrite the text between them.
        out, pos = [], 0
        for m in CODE_SPAN.finditer(line):
            out.append(self.rewrite_prose(source_file, site_file, line[pos:m.start()]))
            out.append(m.group(0))
            pos = m.end()
        out.append(self.rewrite_prose(source_file, site_file, line[pos:]))
        return "".join(out)

    def rewrite_prose(self, source_file, site_file, text):
        text = self.rewrite_text(source_file, site_file, text, INLINE)
        text = self.rewrite_text(source_file, site_file, text, REFDEF)
        return self.rewrite_text(source_file, site_file, text, HTML)

    def rewrite_file(self, source_file, site_file, content):
        lines, fence = [], None
        for line in content.splitlines(keepends=True):
            m = FENCE.match(line)
            if fence:
                if m and m.group(1) == fence:
                    fence = None
                lines.append(line)
            elif m:
                fence = m.group(1)
                lines.append(line)
            else:
                lines.append(self.rewrite_line(source_file, site_file, line))
        return "".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ref", required=True)
    parser.add_argument("--tree", required=True, help="file with every path of the main repository at the ref")
    parser.add_argument("--dest", required=True, help="docs/ directory of this site")
    args = parser.parse_args()

    tree = Path(args.tree).read_text().split("\n")
    tree = [t for t in tree if t]
    rewriter = Rewriter(args.ref, tree)
    dest = Path(args.dest)

    for source_file in sorted(tree):
        site_file = site_path(source_file)
        if not site_file or not source_file.endswith(".md"):
            continue
        path = dest / site_file
        content = path.read_text(encoding="utf-8")
        path.write_text(rewriter.rewrite_file(source_file, site_file, content), encoding="utf-8")

    print(f"rewrite-links: {rewriter.rewritten} links rewritten")
    for source_file, link in rewriter.broken:
        print(f"rewrite-links: broken link in {source_file}: {link}", file=sys.stderr)


if __name__ == "__main__":
    main()
