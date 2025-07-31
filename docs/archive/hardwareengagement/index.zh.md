# 硬件参与

!!! warning "机器翻译声明"
    本文档由 AI 语言模型 (Claude) 从英文自动翻译而成。如发现翻译错误或不准确之处，请在 [Kepler 文档项目](https://github.com/sustainable-computing-io/kepler-doc/issues) 中提交 issue 报告问题。

在本文档中，我们将分享如何让 Kepler 与特定硬件设备集成的步骤。
考虑到有许多不同的硬件设备，我们在当前阶段只会写下主要步骤。
您可以将此作为待办事项列表，逐步让 Kepler 与您自己的硬件设备集成。

## 第 0 阶段 概念验证

在此阶段，我们将专注于可以通过 golang 收集的基本数据，您可以构建在您的
设备上运行良好的自己的 Kepler。以下步骤可以并行运行。

### 二进制构建和容器构建

目前 Kepler 容器镜像来自 GPU 镜像以支持 GPU 用例。考虑到 IOT 设备的一般情况。
您可能需要从 UBI 镜像构建 Kepler。我们建议您按照以下步骤设置本地构建环境并尝试构建。

1. 找一个 Linux 操作系统。
1. 安装 Kepler 依赖项，如 eBPF golang（BCC）、Linux 头文件并构建 Kepler
   （从主分支或最新发布分支）二进制文件。
1. （可选）修改 [dockerfile](https://github.com/sustainable-computing-io/kepler/tree/main/build)
   以构建容器镜像。

### 功耗 API

目前，我们使用功耗 API，如 RAPL 或 ACPI。对于某些设备，您可能需要找到自己的
方法来获取功耗，并在 golang 中实现以供 Kepler 使用。
有关进一步计划，请参考[这里](https://github.com/sustainable-computing-io/kepler/issues/644)

### eBPF 数据

目前，我们依赖 eBPF 获取有关进程的关键 CPU、IRQ 和性能信息。
因此，请参考 [cilium/ebpf](https://github.com/cilium/ebpf) 的文档来测试这些
Go 包在您的设备上是否运行良好。

如果您需要任何进一步的调整，请告诉我们！

## 第 1 阶段 与比率集成

在此阶段，我们将参考 Kepler 模型。集成并实现特定于您的设备的自己的逻辑，
并深入研究功耗 API。

### 范围

您应该知道功耗 API 的范围。您有多少个 API？它是否按 CPU/内存/IO 分类？

### 间隔

您应该知道功耗 API 的间隔。由于 Kepler 默认每 3 秒收集一次 eBPF 数据，
您应该了解间隔并使它们在同一时隙中。

### 验证

您可以交叉检查和验证数据。

## 第 2 阶段 模型训练

待定
