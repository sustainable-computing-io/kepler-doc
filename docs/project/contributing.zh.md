# 贡献指南

我们欢迎社区为Kepler项目贡献任何形式的支持！

如需了解如何入门的详细指南，请查阅[贡献指南](https://github.com/sustainable-computing-io/kepler/blob/main/CONTRIBUTING.md)。

## Kepler采用机构

您或您的组织正在使用Kepler？这太棒了！我们非常希望听到您的反馈！💚

[此处的yaml文件](https://github.com/sustainable-computing-io/kepler-doc/tree/main/data/adopters.yaml)记录了所有Kepler采用机构名单。若您希望将贵组织加入列表，只需在该文件中添加条目，合并后即可在[Kepler采用机构页面](https://sustainable-computing.io/project/adopters/)展示。

### 采用机构页面渲染

当更新[data/adopters.yaml](https://github.com/sustainable-computing-io/kepler-doc/blob/main/data/adopters.yaml)文件添加新机构时，需安装[gomplate](https://docs.gomplate.ca/)工具。Kepler官网使用该工具来正确渲染采用机构页面。

!!! 注意  
    仅当更新[data/adopters.yaml](https://github.com/sustainable-computing-io/kepler-doc/blob/main/data/adopters.yaml)文件添加新机构时才需要以下步骤。

1. 安装pkgx

    ```sh
    curl -Ssf https://pkgx.sh | sh
    ```

2. 安装gomplate

    ```sh
    pkgx +gomplate.ca^v3.11.7
    ```

3. 根据上一步输出更新PATH环境变量。示例：

    ```sh
    PATH="$HOME/.pkgx/gomplate.ca/v3.11.7/bin${PATH:+:$PATH}"
    ```

4. 使用data/adopters.yaml数据更新采用机构页面

    ```sh
    gomplate -d adopters=./data/adopters.yaml -f templates/adopters.md -o docs/project/adopters.md
    ```

### 添加您的组织

请按以下步骤操作：

1. Fork[kepler-doc](https://github.com/sustainable-computing-io/kepler-doc)仓库
1. 本地克隆：`git clone https://github.com/<您的GitHub用户名>/kepler-doc.git`
1. （可选）将组织LOGO添加至docs/fig/logos目录。建议命名格式如MY-ORG.png（默认使用docs/fig/logos/default.svg作为Kepler标识，当未提供组织LOGO时显示）
1. 在YAML文件中添加条目，包含组织名称、官网链接及LOGO路径。示例：

    ```yaml
        - name: Kepler
          url: https://sustainable-computing.io/
          logo: logos/kepler.svg
    ```

1. 通过以下命令验证采用机构页面更新效果（预览文档构建效果详见[安装MkDocs指南](https://github.com/sustainable-computing-io/kepler-doc?tab=readme-ov-file#install-mkdocs)）：

    ```sh
    mkdocs build
    mkdocs server
    ```

1. 确认无误后，使用`git add -A`添加变更文件，并通过`git commit -s -m "将MY-ORG加入采用机构"`提交（需签署提交，参见[Kepler项目的DCO要求](https://github.com/sustainable-computing-io/kepler/blob/main/DCO)）
1. 推送提交：`git push origin main`
1. 向[kepler-doc](https://github.com/sustainable-computing-io/kepler-doc)发起Pull Request