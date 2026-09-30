# 贡献

!!! warning "机器翻译声明"
    本文档由 AI 语言模型 (Claude) 从英文自动翻译而成。如发现翻译错误或不准确之处，请在 [Kepler 文档项目](https://github.com/sustainable-computing-io/kepler-doc/issues) 中提交 issue 报告问题。

我们欢迎社区对 Kepler 的各种贡献！

有关如何开始的深入指南，请查看[这里](https://github.com/sustainable-computing-io/kepler/blob/main/CONTRIBUTING.md)的贡献指南。

## Kepler 采用者

您和您的组织正在使用 Kepler？太棒了。我们很乐意听到您的声音！💚

[这里](https://github.com/sustainable-computing-io/kepler-doc/tree/main/data/adopters.yaml)的 yaml 文件包含所有 Kepler 采用者的列表。
如果您想将您的组织添加到 Kepler 的列表中，只需在那里添加一个条目，合并后您将在[Kepler 采用者](https://sustainable-computing.io/project/adopters/)下找到。

### 渲染采用者

作为将组织添加到 Kepler 采用者页面的一部分，当[data/adopters.yaml](https://github.com/sustainable-computing-io/kepler-doc/blob/main/data/adopters.yaml)更新时，必须安装 [gomplate](https://docs.gomplate.ca/)。
Kepler 网站使用它来正确渲染 Kepler 采用者页面。

!!! note
    只有在作为将组织添加到 Kepler 采用者页面的一部分而更新[data/adopters.yaml](https://github.com/sustainable-computing-io/kepler-doc/blob/main/data/adopters.yaml)时，才需要这些步骤。

1. 安装 pkgx

    ```sh
    curl -Ssf https://pkgx.sh | sh
    ```

1. 安装 gomplate

    ```sh
    pkgx +gomplate.ca^v3.11.7
    ```

1. 输入前一个命令的输出来更新 PATH。示例：

    ```sh
    PATH="$HOME/.pkgx/gomplate.ca/v3.11.7/bin${PATH:+:$PATH}"
    ```

1. 使用 data/adopters.yaml 中的数据更新采用者页面

    ```sh
    gomplate -d adopters=./data/adopters.yaml -f templates/adopters.md -o docs/project/adopters.md
    ```

### 添加您的组织

要这样做，请按照以下步骤操作：

1. Fork [kepler-doc](https://github.com/sustainable-computing-io/kepler-doc) 仓库。
1. 使用 `git clone https://github.com/<YOUR-GH-USERNAME>/kepler-doc.git` 在本地克隆它。
1. （可选）将您组织的 logo 添加到 docs/fig/logos。好的做法是将 logo 命名为例如 MY-ORG.png（=> docs/fig/logos/default.svg 是 Kepler logo，当未提供组织 logo 时使用）。
1. 向 YAML 文件添加一个条目，包含您组织的名称、链接到其网站的 url 和 logo 的路径。示例：

    ```yaml
        - name: Kepler
          url: https://sustainable-computing.io/
          logo: logos/kepler.svg
    ```

1. 通过运行以下命令验证 Kepler 采用者页面正确更新（有关如何从构建预览文档的更多详细信息，请参阅[安装 MkDocs](https://github.com/sustainable-computing-io/kepler-doc?tab=readme-ov-file#install-mkdocs)）：

    ```sh
    mkdocs build
    mkdocs server
    ```

1. 对更改满意后，使用 `git add -A` 添加更改的文件，然后使用 `git commit -s -m "Add MY-ORG to adopters"` 提交（需要提交签名，请参阅 [kepler 项目的 DCO](https://github.com/sustainable-computing-io/kepler/blob/main/DCO)）。
1. 使用 `git push origin main` 推送提交。
1. 向 [kepler-doc](https://github.com/sustainable-computing-io/kepler-doc) 打开 Pull Request

## 文档翻译

Kepler 欢迎贡献将我们的文档翻译成不同语言，以便全球开发者和运维人员社区都能访问！

### 翻译流程概述

我们的文档遵循国际化 (i18n) 约定，使用语言后缀：

- **英文（原始）**：`docs/path/to/file.md`
- **中文**：`docs/path/to/file.zh.md`
- **其他语言**：`docs/path/to/file.[LANG_CODE].md`

### 开始翻译

#### 1. **使用 AI 翻译助手**

为了高效且准确的技术翻译，我们推荐使用我们专门的 AI 翻译提示。这确保：

- ✅ **技术准确性** - 保留 API 名称、命令和代码块
- ✅ **术语一致性** - 在文档间保持技术术语一致
- ✅ **格式正确** - 保持 markdown 结构和语法高亮
- ✅ **质量验证** - 生成质量检查报告

**📋 翻译助手提示**：[TRANSLATOR.md](https://gist.github.com/sthaha/933b47dc19c5bc228c038b09ca5de817)

#### 2. **质量保证流程**

每个翻译都应包含**质量检查报告**以验证准确性：

**每个翻译生成的文件：**

```text
docs/path/to/file.md          # 原始英文
docs/path/to/file.zh.md       # 中文翻译
docs/path/to/file.zh-qc.md    # 质量检查报告
```

质量检查报告（`.zh-qc.md`）包含：

- 原始内容与逆向翻译内容的比较
- 技术准确性评估
- 格式和结构验证
- 批准/修订建议

#### 3. **翻译指南**

**✅ 应该做的：**

- 保留所有技术标识符（API 名称、命令、URL）
- 维护 markdown 格式和代码块语法
- 在文档内部和跨文档保持术语一致性
- 包含关于 AI 翻译的法定警告
- 为验证生成质量检查报告

**❌ 不应该做的：**

- 翻译技术命令、API 端点或代码片段
- 修改文件路径、仓库 URL 或外部链接
- 更改文档结构或标题层次
- 跳过质量验证步骤

#### 4. **法定警告要求**

所有翻译文档必须在开头包含此警告：

```markdown
!!! warning "机器翻译声明"
    本文档由 AI 语言模型 (Claude) 从英文自动翻译而成。如发现翻译错误或不准确之处，请在 [Kepler 文档项目](https://github.com/sustainable-computing-io/kepler-doc/issues) 中提交 issue 报告问题。
```

### 贡献您的翻译

#### **分步流程：**

1. **Fork 和克隆**

   ```bash
   git clone https://github.com/<YOUR-USERNAME>/kepler-doc.git
   cd kepler-doc
   ```

2. **创建翻译分支**

   ```bash
   git checkout -b translate-[language]-[document-name]
   ```

3. **生成翻译**
   - 使用 [AI 翻译助手](https://gist.github.com/sthaha/933b47dc19c5bc228c038b09ca5de817)
   - 遵循质量保证流程
   - 确保生成所有文件（`.zh.md` + `.zh-qc.md`）

4. **审查和测试**

   ```bash
   mkdocs build
   mkdocs serve
   ```

   在 `http://localhost:8000` 预览您的翻译

5. **提交更改**

   ```bash
   git add docs/path/to/file.zh.md docs/path/to/file.zh-qc.md
   git commit -s -m "Add Chinese translation for [document-name]

   - Translate docs/path/to/file.md to Chinese
   - Include quality check report for validation
   - Follow i18n conventions with .zh.md suffix"
   ```

6. **打开 Pull Request**
   - 包含翻译和质量检查文件
   - 在 PR 描述中引用质量检查报告发现
   - 提及需要特殊处理的技术术语

### 翻译优先级

**高优先级文档：**

- 安装指南（`docs/kepler/installation/`）
- 使用文档（`docs/kepler/usage/`）
- 配置指南（`docs/kepler-operator/`）

**中等优先级：**

- 开发者文档（`docs/kepler/developer/`）
- 架构和设计文档（`docs/archive/design/`）

### 语言支持

当前支持的语言：

- **中文**：`.zh.md` 后缀

**想要添加新语言？**

1. 查看 [mkdocs.yml i18n 配置](https://github.com/sustainable-computing-io/kepler-doc/blob/main/mkdocs.yml)
2. 打开 issue 讨论语言代码和导航结构
3. 使用适当的语言后缀遵循相同流程

### 翻译维护

在以下情况下应更新翻译：

- 原始英文文档发生重大更改
- 技术 API 或命令被修改
- 添加影响记录程序的新功能

**专业提示**：关注仓库以了解有翻译的英文文件的更改，以保持最新状态！

### 获取帮助

- **关于翻译流程的问题**：[GitHub Discussions](https://github.com/sustainable-computing-io/kepler/discussions)
- **报告翻译错误**：[GitHub Issues](https://github.com/sustainable-computing-io/kepler-doc/issues)
- **技术内容澄清**：[主要 Kepler 仓库](https://github.com/sustainable-computing-io/kepler/discussions)

---

感谢您帮助使 Kepler 文档在全世界都能访问！🌍
