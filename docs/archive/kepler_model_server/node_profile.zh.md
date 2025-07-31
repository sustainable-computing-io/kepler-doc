# 节点配置文件

!!! warning "机器翻译声明"
    本文档由 AI 语言模型 (Claude) 从英文自动翻译而成。如发现翻译错误或不准确之处，请在 [Kepler 文档项目](https://github.com/sustainable-computing-io/kepler-doc/issues) 中提交 issue 报告问题。

我们基于处理器型号、内核数量、芯片数量、内存大小和最大 CPU 频率形成一组机器
（节点），称为[节点类型](./pipeline.md#node-type)。当从裸机收集数据时，这些
属性会自动提取并以 json 格式保存为机器规格。

将为每个节点类型构建一个功率模型。对于每组节点类型，我们制作一个配置文件，
包括在没有用户工作负载时资源使用几乎恒定的背景功率、每个功率组件（例如，
内核、非内核、dram、封装、平台）的最小、最大功率，以及每个
[特征组](./pipeline.md#feature-group)的归一化缩放器（即 MinMaxScaler）、
标准化缩放器（即 StandardScaler）。

节点规格由以下组成：

- processor *- CPU 处理器型号名称*
- cores *- CPU 内核数量*
- chips *- 芯片数量*
- memory_gb *- 内存大小（GB）*
- cpu_freq_mhz *- 最大 CPU 频率（MHz）*
