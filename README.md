# Documentation for Kepler-Doc

Follow [sustainable-computing.io](https://sustainable-computing.io/) to see documentation

## Install MkDocs

**Requirements:**

- Python 3.8

```bash
pip install -r requirements.txt
```

## Rendering adopters

- uses gomplate 3.11.4, either install it or use tea.xyz:

    ```sh
    sh <(curl https://tea.xyz) +gomplate.ca^v3.11.4 sh
    ```

- template adopters via:

    ```sh
    gomplate -d adopters=./data/adopters.yaml -f templates/adopters.md -o docs/project/adopters.md
    ```

## Commands

- `mkdocs new [dir-name]` - Create a new project.
- `mkdocs serve` - Start the live-reloading docs server.
- `mkdocs build` - Build the documentation site.
- `mkdocs -h` - Print help message and exit.

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
    pip install -r requirements.txt
    ```

1. Once built, type `mkdocs serve`
1. A box will appear informing you that the site is available on port `8000`. Click the link to view the site
1. Make your changes as normal to the files within the `docs/` folder. The preview site will live reload
1. When you're satisfied with your updates, commit them to your fork: `git add -A && git commit -sm "docs: a commit message here" && git push`
1. Create a PR and you're done
