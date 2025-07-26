# Kepler 深度解析

## Kepler组件及其功能

Kepler技术栈由Kepler和Kepler模型服务器组成

### Kepler

Kepler（基于Kubernetes的高效能耗监控器）能够估算进程、容器和Kubernetes Pod层级的功耗数据。

**Kepler如何采集数据？**

Kepler通过以下方式采集能耗数据：

#### eBPF与硬件计数器

Kepler通过集成到内核路径的BPF程序获取进程级资源利用率指标，或使用硬件计数器提供的指标。根据系统环境差异，构建模型所使用的指标类型会有所不同。例如，在目标系统中可能使用硬件计数器，也可能使用eBPF等工具提供的指标。

#### 实时组件级功耗计量

Kepler还通过各类API采集节点组件的实时功耗数据：
- 英特尔运行平均功率限制（RAPL）——用于CPU和DRAM功耗
- NVIDIA管理库（NVML）——用于GPU功耗

#### 平台级功耗计量

对于整机平台功耗，Kepler采用：
- 高级配置与电源接口（ACPI）
- Redfish/智能电源管理接口（IPMI）
- 当系统缺乏实时功耗指标时，使用基于回归训练的功耗模型

### Kepler模型服务器

模型服务器用于训练功耗模型，可选择与Kepler协同部署，帮助Kepler根据环境特征（如CPU型号、可用指标和所需模型精度）选择最优模型。
***未来版本中，Kepler将直接集成模型服务器的智能选型逻辑。***

模型服务器通过特定裸金属节点的Prometheus指标进行训练，记录节点总能耗与容器/系统进程（OS及其他后台进程）的资源利用率。容器指标通过运行各类资源压力测试（如使用`stress-ng`工具）获取。模型创建阶段采用回归算法持续训练，直至达到预期精度。

训练完成后，模型通过GitHub仓库发布，供任意Kepler部署下载使用。Kepler基于这些模型，根据资源使用情况计算节点（虚拟机）功耗。需注意模型构建指标会随系统环境变化，可能采用硬件计数器或eBPF等工具提供的指标。

![功耗模型训练](../fig/power_model_training.jpg)

架构细节请参阅[Kepler模型服务器文档](https://sustainable-computing.io/kepler_model_server/architecture/)。

### 系统功耗采集——虚拟机与裸金属对比

Kepler的部署环境不同，系统功耗采集方式也存在差异。如下图所示，Kepler可部署于裸金属或虚拟机环境。

![虚拟机与裸金属对比](../fig/vms_versus_bms.jpg)

#### 直接实时系统功耗采集（裸金属）

在支持直接采集实时系统功耗的裸金属环境中，Kepler可采用比率功耗模型拆分系统资源功耗。实时功耗API输出的绝对功耗包含动态功耗与闲置功耗：动态功耗与资源利用率直接相关，闲置功耗则是系统无论负载与否都存在的恒定功耗。这一区分至关重要，因为两类功耗在进程间的分配机制不同。

#### 估算系统功耗（虚拟机）

公有云虚拟机环境目前无法直接测量单虚拟机功耗，需依赖训练好的功耗模型进行估算，这会引入影响精度的限制条件。

Kepler通过训练模型估算虚拟机的动态功耗，再应用比率功耗模型推算进程级功耗。由于虚拟机通常不提供硬件计数器，Kepler转而使用eBPF指标计算比率。需要强调的是，公有云虚拟机的训练模型无法拆分资源闲置功耗——因为宿主机的并发虚拟机数量不可知。相关限制细节将在后文说明，因此Kepler不会暴露运行于虚拟机的容器的闲置功耗数据。

功耗模型通过对裸金属节点基准测试采集的数据（资源利用率与功耗）进行回归分析（如线性回归或基于机器学习的回归）训练而成。

#### 透传式虚拟机功耗估算

Kepler首先部署于裸金属节点（即云控制平面），通过裸金属的实时功耗数据持续测量各虚拟机的动态/闲置功耗，随后通过["Hypervisor Hypercalls"](https://docs.kernel.org/virt/kvm/x86/hypercalls.html)或cGroup文件等机制将数据透传给虚拟机。虚拟机内的Kepler实例再利用这些功耗数据，应用比率功耗模型估算内部进程的能耗。

!!! 注意
    透传方案目前处于探索阶段，尚未正式发布。

### 比率功耗模型详解

如前所述，动态功耗与资源利用率直接相关，闲置功耗则是恒定值。理解这一区别对进程级功耗分配至关重要。比率功耗模型通过计算进程资源利用率与系统总利用率的比例，乘以资源的动态功耗值，实现精确的功耗估算。例如某程序占用10%CPU资源，即对应消耗10%的CPU总功耗。

闲置功耗分配遵循[温室气体协议指南](https://www.gesi.org/research/ict-sector-guidance-built-on-the-ghg-protocol-product-life-cycle-accounting-and-reporting-standard)，按容器体积占主机总容器体积的比例分摊。值得注意的是，Kepler对不同资源的利用率评估方式各异：裸金属环境中使用硬件计数器（CPU指令评估CPU利用率、缓存未命中评估内存利用率、流式多处理器评估GPU利用率）。

### 功耗归因机制解析

完成数据采集与模型训练后，Kepler通过资源利用率比例拆分各进程的能耗数据，并聚合为容器和Kubernetes Pod层级的功耗指标，最终由Prometheus存储。

Kepler通过BPF程序采集的进程ID（PID）关联容器，再从`/proc/PID/cgroup`获取容器ID后与Kubernetes APIServer的Pod列表匹配。未关联Kubernetes容器的进程归为`系统进程`（包括PID 0）。

***未来版本将支持虚拟机进程与VM ID的关联，实现虚拟机级指标导出。***

### 预训练模型的局限性

相比实时功耗模型，预训练模型存在以下限制：

- **系统特异性**：预训练模型与CPU型号和架构强相关。虽然通用模型能提供应用功耗的参考，但精度有限。
- **虚拟机功耗高估**：单虚拟机直接套用裸金属模型会导致高估，因为多虚拟机共享节点时的实际功耗曲线会变化。
- **闲置功耗分配难题**：公有云环境无法确定宿主机的并发虚拟机数量，导致按体积比例分摊闲置功耗的机制难以准确实施。
- **依赖Hypervisor报告**：虚拟机模型的准确性受限于Hypervisor对CPU寄存器值的报告质量，资源超分场景会影响指标可靠性。

!!! 注意
    预训练模型限制的详细分析请参阅Kepler维护者的[技术博客](https://www.cncf.io/blog/2023/10/11/exploring-keplers-potentials-unveiling-cloud-application-power-consumption/)。

- [ ] 解释[模型库](https://github.com/sustainable-computing-io/kepler-model-server/tree/main/tests/test_models)中不同模型的适用场景与选择策略
- [ ] AbsComponentModelWeight
- [ ] AbsComponentPower
- [ ] AbsModelWeight
- [ ] AbsPower
- [ ] DynComponentModelWeight
- [ ] DynComponentPower
- [ ] XGBoost