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

## Documentation Translation

Kepler welcomes contributions to translate our documentation into different languages to make it accessible to a global community of developers and operators!

### Translation Process Overview

Our documentation follows internationalization (i18n) conventions using language suffixes:

- **English (Original)**: `docs/path/to/file.md`
- **Chinese**: `docs/path/to/file.zh.md`
- **Other languages**: `docs/path/to/file.[LANG_CODE].md`

### Getting Started with Translations

#### 1. **Use the AI Translation Agent**

For efficient and accurate technical translations, we recommend using our specialized AI translation prompt. This ensures:

- ✅ **Technical accuracy** - Preserves API names, commands, and code blocks
- ✅ **Consistent terminology** - Maintains technical terms across documents
- ✅ **Proper formatting** - Keeps markdown structure and syntax highlighting
- ✅ **Quality validation** - Generates quality check reports

**📋 Translation Agent Prompt**: [TRANSLATOR.md](https://gist.github.com/sthaha/933b47dc19c5bc228c038b09ca5de817)

#### 2. **Quality Assurance Process**

Every translation should include a **quality check report** to validate accuracy:

**Generated Files for Each Translation:**

```text
docs/path/to/file.md          # Original English
docs/path/to/file.zh.md       # Chinese translation
docs/path/to/file.zh-qc.md    # Quality check report
```

The quality check report (`.zh-qc.md`) contains:

- Comparison between original and reverse-translated content
- Technical accuracy assessment
- Formatting and structure validation
- Recommendation for approval/revision

#### 3. **Translation Guidelines**

**✅ DO:**

- Preserve all technical identifiers (API names, commands, URLs)
- Maintain markdown formatting and code block syntax
- Keep consistent terminology within and across documents
- Include the statutory warning about AI translation
- Generate quality check reports for validation

**❌ DON'T:**

- Translate technical commands, API endpoints, or code snippets
- Modify file paths, repository URLs, or external links
- Change the document structure or heading hierarchy
- Skip quality validation steps

#### 4. **Statutory Warning Requirement**

All translated documents must include this warning at the beginning:

```markdown
!!! warning "机器翻译声明"
    本文档由 AI 语言模型 (Claude) 从英文自动翻译而成。如发现翻译错误或不准确之处，请在 [Kepler 文档项目](https://github.com/sustainable-computing-io/kepler-doc/issues) 中提交 issue 报告问题。
```

### Contributing Your Translation

#### **Step-by-Step Process:**

1. **Fork and Clone**

   ```bash
   git clone https://github.com/<YOUR-USERNAME>/kepler-doc.git
   cd kepler-doc
   ```

2. **Create Translation Branch**

   ```bash
   git checkout -b translate-[language]-[document-name]
   ```

3. **Generate Translation**
   - Use the [AI translation agent](https://gist.github.com/sthaha/933b47dc19c5bc228c038b09ca5de817)
   - Follow the quality assurance process
   - Ensure all files are generated (`.zh.md` + `.zh-qc.md`)

4. **Review and Test**

   ```bash
   mkdocs build
   mkdocs serve
   ```

   Preview your translations at `http://localhost:8000`

5. **Commit Changes**

   ```bash
   git add docs/path/to/file.zh.md docs/path/to/file.zh-qc.md
   git commit -s -m "Add Chinese translation for [document-name]

   - Translate docs/path/to/file.md to Chinese
   - Include quality check report for validation
   - Follow i18n conventions with .zh.md suffix"
   ```

6. **Open Pull Request**
   - Include both translation and quality check files
   - Reference the quality check report findings in PR description
   - Mention any technical terms that required special handling

### Translation Priority

**High Priority Documents:**

- Installation guides (`docs/kepler/installation/`)
- Usage documentation (`docs/kepler/usage/`)
- Configuration guides (`docs/kepler-operator/`)

**Medium Priority:**

- Developer documentation (`docs/kepler/developer/`)
- Architecture and design docs (`docs/archive/design/`)

### Language Support

Currently supported languages:

- **中文 (Chinese)**: `.zh.md` suffix

**Want to add a new language?**

1. Check [mkdocs.yml i18n configuration](https://github.com/sustainable-computing-io/kepler-doc/blob/main/mkdocs.yml)
2. Open an issue to discuss language code and navigation structure
3. Follow the same process with appropriate language suffix

### Translation Maintenance

Translations should be updated when:

- Original English documents are significantly changed
- Technical APIs or commands are modified
- New features are added that affect documented procedures

**Pro tip**: Watch the repository for changes to English files that have translations to stay up-to-date!

### Getting Help

- **Questions about translation process**: [GitHub Discussions](https://github.com/sustainable-computing-io/kepler-doc/discussions)
- **Report translation errors**: [GitHub Issues](https://github.com/sustainable-computing-io/kepler-doc/issues)
- **Technical content clarification**: [Main Kepler Repository](https://github.com/sustainable-computing-io/kepler/discussions)

---

Thank you for helping make Kepler documentation accessible worldwide! 🌍
