# Contributing

We welcome all kinds of contributions to Kepler from the community!

For an in-depth guide on how to get started, checkout the Contributing Guide [here](https://github.com/sustainable-computing-io/kepler/blob/main/CONTRIBUTING.md).

# Kepler adopters

You and your organisation are using Kepler? That’s awesome. We would love to hear from you! 💚

## Adding your organisation

The yaml file in [here](https://github.com/sustainable-computing-io/kepler-doc/tree/main/data/adopters.yaml) contains a list of all Kepler adopters.

If you want to add yourself just add an entry there and once merged you will be found under [adopters](https://sustainable-computing.io/project/adopters/).

To do so follow these steps:

1. Fork the [kepler-doc](https://github.com/sustainable-computing-io/kepler-doc) repository.
2. Clone it locally with `git clone https://github.com/<YOUR-GH-USERNAME>/kepler-doc.git`.
3. (Optional) Add the logo of your organisation to docs/fig/logos. Good practice is for the logo to be called e.g. MY-ORG.png (=> docs/fig/logos/default.svg is the Kepler logo, it is used when no organisation logo is provided.)
4. Add an entry to the YAML file with the name of your organisation, url that links to its website, and the path to the logo. Example:
```
    - name: Kepler
      url: https://sustainable-computing.io/
      logo: logos/kepler.svg
```
5. Save the file, then do `git add -A` and commit using `git commit -s -m "Add MY-ORG to adopters"` (commit signoff is required, see [DCO of the kepler project](https://github.com/sustainable-computing-io/kepler/blob/main/DCO)).
6. Push the commit with `git push origin main`.
7. Open a Pull Request to [kepler-doc](https://github.com/sustainable-computing-io/kepler-doc)