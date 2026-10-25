"""Build the Material blog for the default language only.

The blog plugin resolves the blog index and its posts in on_files and holds on
to their File objects. mkdocs-static-i18n runs on_files after it and returns
new File objects for each language, so the blog plugin updates files that are
no longer part of the site: posts never get built and the index renders as a
plain page. For the default language, this hook points each blog page at the
file the i18n plugin kept. For other languages, it drops the blog pages and
the Blog nav entry. The i18n plugin lists a zh alternate for each blog page, so
the default build also prunes the alternates to the default language. The
language switcher then falls back to the zh home page.

Generated views (archive, categories, pagination) have no source file, so the
i18n plugin drops them. mkdocs.yml disables them.

See https://github.com/squidfunk/mkdocs-material/issues/5909
"""

from __future__ import annotations

from mkdocs.plugins import event_priority

_nav: list | None = None


def _is_blog(item) -> bool:
    return isinstance(item, dict) and "Blog" in item


@event_priority(-110)
def on_files(files, config):
    """Run after mkdocs-static-i18n (-100) to re-link or drop blog pages."""
    global _nav
    blog = config.plugins.get("material/blog")
    i18n = config.plugins.get("i18n")
    if not blog or not blog.config.enabled or not i18n:
        return files

    if _nav is None:
        _nav = config.nav
    blog_dir = blog.config.blog_dir.rstrip("/") + "/"

    if not i18n.is_default_language_build:
        config.nav = [item for item in _nav if not _is_blog(item)]
        for file in [f for f in files if f.src_uri.startswith(blog_dir)]:
            files.remove(file)
        return files

    config.nav = _nav
    for page in [blog.blog, *blog.blog.posts]:
        file = files.get_file_from_path(page.file.src_uri)
        if file is None or file is page.file:
            continue
        file.page = page
        page.file = file
    return files


@event_priority(-110)
def on_nav(nav, config, files):
    """Run after mkdocs-static-i18n (-100) to drop alternates of blog pages."""
    blog = config.plugins.get("material/blog")
    i18n = config.plugins.get("i18n")
    if not blog or not blog.config.enabled or not i18n:
        return nav

    if i18n.is_default_language_build:
        blog_dir = blog.config.blog_dir.rstrip("/") + "/"
        for file in files:
            if file.src_uri.startswith(blog_dir):
                file.alternates = {
                    lang: alt
                    for lang, alt in file.alternates.items()
                    if lang == i18n.current_language
                }
    return nav
