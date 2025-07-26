# Kepler 能源数据源

## 背景

### RAPL - 运行平均功率限制

英特尔运行平均功率限制（RAPL）是一项硬件特性，可用于监测CPU芯片不同区域、连接的内存以及集成GPU的能耗。该特性首次出现在英特尔Sandy Bridge架构中，并在后续处理器架构中持续演进。通过RAPL可以编程获取CPU封装及其组件，以及CPU管理的内存（DRAM）的实时功耗数据。

RAPL提供两大功能：

1. 支持以极细粒度和高采样率测量能耗
2. 允许限制（或封顶）处理器内部不同组件的平均功耗，从而控制处理器的热输出

Kepler利用了RAPL的能耗测量能力。

RAPL支持多个电源域（power domain）。RAPL电源域是具有物理意义的电源管理区域（如处理器封装、DRAM等），每个电源域提供该区域的能耗数据。

RAPL提供以下电源域用于测量和限制能耗：

- **Package（封装）**：测量整个CPU插槽的能耗，包含所有核心、集成显卡以及非核心组件（末级缓存、内存控制器）的能耗。
- **Power Plane 0（PP0）**：测量插槽上所有处理器核心的能耗。
- **Power Plane 1（PP1）**：测量插槽上处理器图形单元（GPU）的能耗（仅限桌面型号）。
- **DRAM**：测量集成内存控制器所连接内存（RAM）的能耗。

不同处理器型号支持的电源域可能有所差异。

## 读取能耗值

Kepler按以下优先级顺序选择能源数据源：

1. Sysfs接口
2. MSR寄存器
3. Hwmon驱动

### 使用RAPL Sysfs接口

从Linux内核3.13版本开始，可通过`Power Capping Framework`[2]读取RAPL数据。

Linux电源封顶框架通过sysfs以树形对象结构向用户空间暴露电源封顶设备。

该sysfs树挂载在`/sys/class/powercap/intel-rapl`路径下。当RAPL可用时，此路径存在，Kepler从此路径读取能耗值。

### 使用RAPL MSR（模型特定寄存器）

RAPL能耗计数器可通过模型特定寄存器（MSRs）访问。这些32位寄存器记录了自处理器启动以来的能耗值，约每毫秒更新一次。能耗值以特定于处理器型号的能量单位计量：Sandy Bridge使用15.3微焦耳单位，而Haswell和Skylake使用61微焦耳单位。在进行能耗计算前，可通过特定MSR读取能量单位。

在Linux系统上，可通过内核msr驱动直接访问MSR。直接从MSR读取RAPL域值需要先检测CPU型号并读取RAPL能量单位，然后通过读取对应`MSR状态`寄存器获取每个CPU封装的RAPL域数据。

RAPL事件主要报告两类数据：
静态事件：热设计规格、最大/最小功率限制和时间窗口
动态事件：来自芯片的RAPL域能耗读数（如PKG、PP0、PP1或DRAM）

### 使用xgene-hwmon内核驱动

通过Xgene-hwmon驱动，Kepler可从APM X-Gene SoC读取功耗数据。该驱动支持以微瓦为单位读取CPU和IO功耗。

### 使用eBpf perf事件

Kepler未使用此方式。

### 使用PAPI库

Kepler未使用性能应用编程接口（PAPI）。

## 所需权限

### Sysfs（powercap）

使用powercap驱动需要root权限。

### MSR寄存器

使用msr驱动需要root权限。

## 参考文献

[1] [RAPL实战：使用RAPL进行功耗测量的经验](https://helda.helsinki.fi/server/api/core/bitstreams/bdc6c9a5-74d4-494b-ae83-860625a665ce/content)

[2] [RA电源封顶框架](https://www.kernel.org/doc/html/next/power/powercap/powercap.html)

[3] [RA内核驱动xgene-hwmon](https://docs.kernel.org/hwmon/xgene-hwmon.html)

[4] [RA性能应用编程接口(PAPI)](https://icl.utk.edu/papi/)