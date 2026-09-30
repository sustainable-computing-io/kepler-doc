# Documentation for Kepler-Doc

[![Netlify Status](https://api.netlify.com/api/v1/badges/89ddb0b5-1814-42dc-bd62-78e472af85e1/deploy-status)](https://app.netlify.com/projects/sustainable-computing/deploys)

Follow [sustainable-computing.io](https://sustainable-computing.io/) to see the Kepler
documentation.
For developing the project's documentation we recommend using either a Dev Container, Running Locally or in Github Codespaces. Choose whichever you prefer.

## Running in Dev Container

This repo ships a [Dev Container](https://containers.dev/) configuration
(`.devcontainer/`) that pins the exact Python and gomplate versions used in CI
(`pr.yaml`, `mkdocs-ghpages.yaml`), plus pre-commit hooks — so what passes
locally passes in CI too.

### Quick start

1. Install the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
   in VS Code (or configure your editor of choice for `containers.dev`).
2. Open the Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`) and run:
   **`Dev Containers: Clone Repository in Named Container Volume...`**
3. When prompted for the repository, use your forked version and named the Volume as you like.
4. VS Code builds the container and clones the repo directly into a named
   volume. On first build, `postCreateCommand` installs dependencies,
   pre-commit hooks, and generates `docs/project/adopters.md` — you'll see a
   summary printed once it's ready.
5. Run `mkdocs serve` inside the container and open the forwarded port
   (`8000`) to preview the docs with hot-reload.

### Why a named volume, not a bind mount?

The default "Reopen in Container" flow bind-mounts your local checkout
directly into the container. That works fine on Linux, but causes real
problems elsewhere (Windows for example):

- **Docker Desktop (macOS/Windows):** bind mounts go through a filesystem
  translation layer to the Linux VM Docker runs in, which can make builds and
  file I/O noticeably slower.
- **Podman (rootless):** bind mounts hit UID/GID mapping issues between your
  host user and the container user, which shows up as random permission
  errors or files owned by `nobody`.

A named volume avoids both: Docker/Podman manage the volume internally,
without translating or remapping your host filesystem. This is why the repo's
`devcontainer.json` sets `workspaceMount` to a named volume by default — it's
the safer choice across platforms, with no real downside on Linux either.

The trade-off: a named volume starts empty, so you clone *into* it via
**Clone Repository in Named Container Volume**, rather than opening an
already-cloned local folder.

### Using Podman instead of Docker

The dev container config works with Podman without changes, but Podman
itself needs to be told to VS Code:

1. In VS Code `settings.json`, set:

```json
   "dev.containers.dockerPath": "podman"
```

1. Restart VS Code after changing this.

This is a per-user editor setting, not something the repo can configure for
you.

**Apple Silicon / ARM note:** gomplate is installed for the container's
target architecture (`linux-amd64` or `linux-arm64`) at build time via
BuildKit's `TARGETARCH`, so this works natively on ARM hosts — no emulation
needed on Podman or Docker Desktop with Apple Silicon.

## Running Locally

### Install MkDocs

Make sure `Python 3.11` or greater is installed, as the CI uses it, then run:

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
