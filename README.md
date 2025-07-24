# Documentation for Kepler-Doc

Follow [sustainable-computing.io](https://sustainable-computing.io/) to see the Kepler
documentation.

## Install MkDocs

Make sure `Python 3.8` or greater is installed, then run:

```bash
# Recommended: Use hatch for integrated development environment
hatch shell

# Alternative: Install with pyproject.toml manually
pip install -e .

# Alternative with uv (faster, modern package manager)
uv sync

```

## mkdocs Commands

To build the documentation site, simply run:

```sh
mkdocs build
```

To preview the documentation from a build on a local machine, start the mkdocs dev-server with
the command below, then open up `http://127.0.0.1:8000/` in your browser, and you'll see the default
home page being displayed:

```sh
mkdocs serve
```

To preview the documentation from a build on a remote machine, start the mkdocs dev-server with
the command below, then open up `http://<ServerIP>:8000/` in your browser, and you'll see the default
home page being displayed.
Make sure port `8000` (or different port of choice) is opened up on the machine running the command
below on:

```sh
mkdocs serve -a 0.0.0.0:8000
```

## Layout

The website layout can be found in [./mkdocs.yml](mkdocs.yml).

## Running in GitHub Codespaces

GitHub codespaces is a pre-configured, virtual, temporary and throwaway environment that you can use to build, modify and contribute to the Kepler docs.
GitHub codespaces [provides a generous free tier](https://github.com/features/codespaces) but always delete your environment after use to avoid bill shock.

1. Fork this repo
1. In your fork, click the green `Code` button
1. Switch across to the Codespaces tab
1. Click "Create codespace on main"
1. A new tab will open and your environment will be built
1. Create `virtualenv` to install `mkdocs`

    ```bash
    virtualenv .venv
    source .venv/bin/activate
    # Recommended: Use hatch
    hatch shell
    # OR manual installation
    pip install -e .
    ```

1. Once built, type `mkdocs serve`
1. A box will appear informing you that the site is available on port `8000`. Click the link to view the site
1. Make your changes as normal to the files within the `docs/` folder. The preview site will live reload
1. When you're satisfied with your updates, commit them to your fork: `git add -A && git commit -sm "docs: a commit message here" && git push`
1. Create a PR and you're done

## Lint Checker

When a Pull Request is pushed to `kepler-doc`, CI runs [Super-Linter](https://github.com/super-linter/super-linter).
To run locally and verify there are no lint errors before pushing, run:

```sh
docker run -e RUN_LOCAL=true -e DEFAULT_BRANCH=main -e LINTER_RULES_PATH=/ -e VALIDATE_MARKDOWN=true -e VALIDATE_ALL_CODEBASE=true -v /path/to/kepler-doc:/tmp/lint --rm ghcr.io/super-linter/super-linter:v6.3.0
```

Replacing `/path/to/kepler-doc` with local path.
This command checks all files via `-e VALIDATE_ALL_CODEBASE=true`.
Upstream only checks modified files, but it is recommended to fix all lint errors.
