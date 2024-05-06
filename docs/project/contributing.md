# Contributing

We welcome all kinds of contributions to Kepler from the community!

For an in-depth guide on how to get started, checkout the Contributing Guide
[here](https://github.com/sustainable-computing-io/kepler/blob/main/CONTRIBUTING.md).

## Kepler Adopters

You and your organization are using Kepler? That's awesome. We would love to hear from you! 💚

The yaml file in [here](https://github.com/sustainable-computing-io/kepler-doc/tree/main/data/adopters.yaml)
contains a list of all Kepler adopters.
If you want to add your organization to Kepler's list, just add an entry there and once merged you will be found under
[Kepler Adopters](https://sustainable-computing.io/project/adopters/).

### Rendering Adopters

As part of adding an organization to the Kepler Adopters page, when
[data/adopters.yaml](https://github.com/sustainable-computing-io/kepler-doc/blob/main/data/adopters.yaml)
is updated, [gomplate](https://docs.gomplate.ca/) must be installed.
The Kepler website uses it to render the Kepler Adopters page properly.

!!! note
    These steps are only needed if
    [data/adopters.yaml](https://github.com/sustainable-computing-io/kepler-doc/blob/main/data/adopters.yaml)
    is updated as part of adding an organization to the Kepler Adopters page.

1. Install pkgx

    ```sh
    curl -Ssf https://pkgx.sh | sh
    ```

1. Install gomplate

    ```sh
    pkgx +gomplate.ca^v3.11.7
    ```

1. Enter the output from the previous command to update PATH. Example:

    ```sh
    PATH="$HOME/.pkgx/gomplate.ca/v3.11.7/bin${PATH:+:$PATH}"
    ```

1. Update adopters page using data from data/adopters.yaml

    ```sh
    gomplate -d adopters=./data/adopters.yaml -f templates/adopters.md -o docs/project/adopters.md
    ```

### Adding Your Organization

To do so follow these steps:

1. Fork the [kepler-doc](https://github.com/sustainable-computing-io/kepler-doc) repository.
1. Clone it locally with `git clone https://github.com/<YOUR-GH-USERNAME>/kepler-doc.git`.
1. (Optional) Add the logo of your organization to docs/fig/logos. Good practice is for the logo to be called e.g. MY-ORG.png (=> docs/fig/logos/default.svg is the Kepler logo, it is used when no organization logo is provided.)
1. Add an entry to the YAML file with the name of your organization, url that links to its website, and the path to the logo. Example:

    ```yaml
        - name: Kepler
          url: https://sustainable-computing.io/
          logo: logos/kepler.svg
    ```

1. Verify the Kepler Adopters page updated properly by running the following commands (see
   [Install MkDocs](https://github.com/sustainable-computing-io/kepler-doc?tab=readme-ov-file#install-mkdocs)
   for more details on how to preview the documentation from a build):

    ```sh
    mkdocs build
    mkdocs server
    ```

1. When happy with the changes, add the changed files using `git add -A` and then commit using
   `git commit -s -m "Add MY-ORG to adopters"` (commit sign-off is required, see
   [DCO of the kepler project](https://github.com/sustainable-computing-io/kepler/blob/main/DCO)).
1. Push the commit with `git push origin main`.
1. Open a Pull Request to [kepler-doc](https://github.com/sustainable-computing-io/kepler-doc)
