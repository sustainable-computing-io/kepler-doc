# 硬件接入指南

本文档将分享如何让Kepler与特定硬件设备对接的步骤。考虑到硬件设备的多样性，我们目前仅提供主要步骤框架。您可将此文档作为待办清单，逐步完成Kepler与您硬件的对接工作。

## 阶段0：可行性验证

本阶段聚焦于通过Golang收集基础数据，并构建可在您设备上运行的Kepler版本。以下步骤可并行执行。

### 二进制构建与容器构建

当前Kepler容器镜像是基于GPU镜像构建的。针对物联网设备的通用场景，您可能需要基于UBI镜像构建。建议按以下步骤设置本地构建环境：

1. 准备Linux操作系统环境
1. 安装Kepler依赖项（包括eBPF golang(BCC)、Linux头文件等），并构建Kepler二进制文件（可从main分支或最新release分支构建）
1. （可选）修改[dockerfile](https://github.com/sustainable-computing-io/kepler/tree/main/build)构建容器镜像

### 功耗数据接口

当前我们使用RAPL或ACPI作为功耗数据接口。某些设备可能需要您自行实现获取功耗数据的Golang接口。远期规划请参考[此issue](https://github.com/sustainable-computing-io/kepler/issues/644)

### eBPF数据采集

当前我们依赖eBPF技术获取进程的关键CPU、中断和性能数据。请参考[cilium/ebpf](https://github.com/cilium/ebpf)文档测试这些Go包在您设备上的运行情况。

如需进一步调整请随时告知！

## 阶段1：能效比集成

本阶段将重构Kepler模型，针对您的设备实现专用逻辑，并深入整合功耗数据接口。

### 接口范围

需明确功耗数据接口的覆盖范围：
- 包含哪些子接口？
- 是否按CPU/内存/IO分类？

### 采集间隔

需了解功耗接口的数据采集频率。Kepler默认每3秒收集一次eBPF数据，需确保时间窗口对齐。

### 数据验证

需进行数据交叉验证确保准确性。

## 阶段2：模型训练

（待补充）