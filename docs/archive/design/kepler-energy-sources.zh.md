# Kepler 能源来源

!!! warning "机器翻译声明"
    本文档由 AI 语言模型 (Claude) 从英文自动翻译而成。如发现翻译错误或不准确之处，请在 [Kepler 文档项目](https://github.com/sustainable-computing-io/kepler-doc/issues) 中提交 issue 报告问题。

## 背景

### RAPL - 运行平均功率限制

Intel 的运行平均功率限制（Running Average Power Limit，RAPL）是一个硬件功能，
允许监控 CPU 芯片不同域、连接的 DRAM 和片上 GPU 的能耗。该功能在 Intel 的
Sandy Bridge 架构中首次引入，并在 Intel 后续处理器架构版本中不断演进。通过 RAPL，
可以编程方式实时获取 CPU 封装及其组件以及 CPU 管理的 DRAM 内存的功耗数据。

RAPL 提供两种不同的功能：

1. 允许以非常精细的粒度和高采样率测量能耗。
2. 允许限制（或上限）处理器内不同组件的平均功耗，这也限制了处理器的热输出。

Kepler 利用了能耗测量功能。

RAPL 支持多个功率域。RAPL 功率域是在功率管理方面具有物理意义的域
（例如，处理器封装、DRAM 等）。每个功率域报告该域的能耗。

RAPL 为测量和限制能耗提供以下功率域：

- **封装**：封装（PKG）域测量整个插槽的能耗。它包括所有内核、集成显卡以及
  非内核组件（最后级缓存、内存控制器）的消耗。
- **功率平面 0**（PP0）：测量插槽上所有处理器内核的能耗。
- **功率平面 1**（PP1）：测量插槽上处理器显卡（GPU）的能耗（仅限桌面型号）。
- **DRAM**：测量连接到集成内存控制器的随机存取内存（RAM）的能耗。

不同功率域的支持因处理器型号而异。

## 读取能量值

Kepler 按以下优先级顺序选择使用一种能源来源：

1. Sysfs
2. MSR
3. Hwmon

### 使用 RAPL Sysfs

从 Linux 内核版本 3.13 开始，可以使用`功率限制框架`[2] 读取 RAPL 值。

Linux 功率限制框架通过 sysfs 以对象树的形式向用户空间公开功率限制设备。

此 sysfs 树挂载在 `/sys/class/powercap/intel-rapl`。当 RAPL 可用时，
此路径存在，Kepler 从该路径读取能量值。

### 使用 RAPL MSR（模型特定寄存器）

RAPL 能量计数器可以通过模型特定寄存器（MSR）访问。计数器是 32 位寄存器，
指示自处理器启动以来消耗的能量。计数器大约每毫秒更新一次。能量以模型特定
能量单位的倍数计算。Sandy Bridge 使用 15.3 微焦耳的能量单位，而 Haswell
和 Skylake 使用 61 微焦耳的单位。在进行能量计算之前，可以从特定的 MSR 读取单位。

在 Linux 上可以使用内核中的 msr 驱动程序直接访问 MSR。直接从 MSR 读取 RAPL
域值需要检测 CPU 型号并在读取 RAPL 域之前读取 RAPL 能量单位。一旦检测到 CPU
型号，就可以通过读取相应的 `MSR 状态` 寄存器按 CPU 封装读取 RAPL 域。

RAPL 事件报告基本上有两种类型的事件：
静态事件：热规格、最大和最小功率上限以及时间窗口。
动态事件：来自芯片的 RAPL 域能量读数，如 PKG、PP0、PP1 或 DRAM

### 使用内核驱动程序 Xgene-hwmon

使用 Xgene-hwmon 驱动程序，Kepler 从 APM X-Gene SoC 读取功率。它支持读取
以微瓦为单位的 CPU 和 IO 功率。

### 使用 eBpf perf 事件

在 Kepler 中未使用。

### 使用 PAPI 库

性能应用程序编程接口（Performance Application Programming Interface，PAPI）
在 Kepler 中未使用。

## 所需权限

### Sysfs（powercap）

使用 powercap 驱动程序需要 root 访问权限。

### MSR

使用 msr 驱动程序需要 root 访问权限。

## 参考资料

[1] [RAPL in Action: Experiences in Using RAPL for Power Measurements](https://helda.helsinki.fi/server/api/core/bitstreams/bdc6c9a5-74d4-494b-ae83-860625a665ce/content)

[2] [RA Power Capping Framework](https://www.kernel.org/doc/html/next/power/powercap/powercap.html)

[3] [RA Kernel driver xgene-hwmon](https://docs.kernel.org/hwmon/xgene-hwmon.html)

[4] [RA Performance Application Programming Interface (PAPI)](https://icl.utk.edu/papi/)
