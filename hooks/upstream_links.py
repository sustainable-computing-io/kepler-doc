"""Rewrite relative links in pages that come from a git submodule.

Pages pulled from a code repo (e.g. kepler) are written for GitHub, so their
relative links are relative to the file inside that repo. Once the page is
symlinked into docs/, two kinds of links break:

* links to other upstream pages that are also published on the site, but under
  a different path;
* links to files that are not part of the site (hack/config.yaml,
  CONTRIBUTING.md, images next to the page, ...).

The first kind is rewritten to the published page, so MkDocs resolves it as a
normal internal link. The second kind is rewritten to the file on GitHub, at
the commit the submodule is pinned to (its tag when it has one).

Pages that do not come from a submodule are left untouched.
"""

from __future__ import annotations

import logging
import os
import re
import subprocess
from functools import lru_cache
from pathlib import Path, PurePosixPath
from urllib.parse import urlsplit

log = logging.getLogger("mkdocs.hooks.upstream_links")

# [text](target) and ![alt](target), with an optional "title".
LINK_RE = re.compile(r'(?P<bang>!?)\[(?P<text>[^\]]*)\]\((?P<target>[^)\s]+)(?P<title>\s+"[^"]*")?\)')
FENCE_RE = re.compile(r"^\s*(```|~~~)")

_site_files: dict[Path, str] = {}


def on_files(files, config):
    """Map the real path of every site file to its path inside docs_dir."""
    _site_files.clear()
    for f in files:
        if f.abs_src_path:
            _site_files[Path(f.abs_src_path).resolve()] = f.src_uri
    return files


def _git(root: Path, *args: str) -> str:
    out = subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True)
    return out.stdout.strip() if out.returncode == 0 else ""


@lru_cache(maxsize=None)
def _submodule_roots(repo_root: Path) -> tuple[Path, ...]:
    """Resolved paths of the submodules declared in repo_root/.gitmodules."""
    gitmodules = repo_root / ".gitmodules"
    if not gitmodules.is_file():
        return ()
    out = _git(repo_root, "config", "--file", str(gitmodules), "--get-regexp", r"\.path$")
    roots = []
    for line in out.splitlines():
        rel = line.split(" ", 1)[1].strip() if " " in line else ""
        if rel:
            roots.append((repo_root / rel).resolve())
    return tuple(roots)


def _submodule_root(real: Path, repo_root: Path) -> Path | None:
    """Return the submodule checkout that contains real, or None.

    A page counts as upstream only when its real path is under a path declared
    in the repo's .gitmodules. That removes the nearest-.git guess, so an
    unrelated parent repository cannot trigger link rewrites.
    """
    for sub in _submodule_roots(repo_root):
        if real == sub or sub in real.parents:
            return sub
    return None


@lru_cache(maxsize=None)
def _upstream(root: Path) -> tuple[str, str] | None:
    """Return (https repo url, ref) for a submodule checkout."""
    url = _git(root, "config", "--get", "remote.origin.url")
    ref = _git(root, "describe", "--tags", "--exact-match", "HEAD") or _git(root, "rev-parse", "HEAD")
    if not url or not ref:
        return None
    url = re.sub(r"^git@github\.com:", "https://github.com/", url)
    return url.removesuffix(".git"), ref


def _rewrite(target: str, image: bool, src_uri: str, real: Path, root: Path, upstream: tuple[str, str]) -> str:
    parts = urlsplit(target)
    if parts.scheme or parts.netloc or target.startswith(("#", "/")) or not parts.path:
        return target
    fragment = f"#{parts.fragment}" if parts.fragment else ""

    dest = (real.parent / parts.path).resolve()
    if dest.is_dir() and (dest / "index.md").exists():
        dest = dest / "index.md"

    if dest in _site_files:
        rel = os.path.relpath(_site_files[dest], str(PurePosixPath(src_uri).parent))
        return Path(rel).as_posix() + fragment

    try:
        repo_path = dest.relative_to(root).as_posix()
    except ValueError:
        return target  # points outside the submodule, leave it alone
    if not dest.exists():
        return target

    url, ref = upstream
    kind = "raw" if image else ("tree" if dest.is_dir() else "blob")
    return f"{url}/{kind}/{ref}/{repo_path}{fragment}"


def on_page_markdown(markdown, page, config, files):
    real = Path(page.file.abs_src_path).resolve()
    repo_root = Path(config["config_file_path"]).resolve().parent
    root = _submodule_root(real, repo_root)
    if root is None:
        return markdown
    upstream = _upstream(root)
    if upstream is None:
        log.warning("Cannot read the git remote/ref of %s, links left as is", root)
        return markdown

    out, in_fence = [], False
    for line in markdown.splitlines(keepends=True):
        if FENCE_RE.match(line):
            in_fence = not in_fence
        if not in_fence:
            line = LINK_RE.sub(
                lambda m: "{}[{}]({}{})".format(
                    m["bang"],
                    m["text"],
                    _rewrite(m["target"], bool(m["bang"]), page.file.src_uri, real, root, upstream),
                    m["title"] or "",
                ),
                line,
            )
        out.append(line)
    return "".join(out)
