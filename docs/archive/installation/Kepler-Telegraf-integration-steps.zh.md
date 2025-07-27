# 简介

Kepler（基于Kubernetes的高效功耗监控导出器）是一款Prometheus导出器。它利用eBPF技术采集CPU性能计数器与Linux内核跟踪点数据[\[1\]](#references)，而Telegraf则是一个用于收集、处理、聚合和写入指标的代理程序[\[2\]](#references)。本文档将介绍如何将Telegraf与Kepler进行集成。

## 集成Telegraf与Kepler的优势

通过将Telegraf与Kepler集成，用户可以在Kepler提供的容器和节点指标基础上，进一步获取平台级监控数据。例如：
- 使用IPMI传感器插件采集电源供应器电流输出百分比等指标
- 获取目前Kepler尚不支持的DPDK相关指标

通过关联分析Kepler提供的功耗/CPU使用指标与Telegraf采集的DPDK指标，用户可以更深入理解网络数据包处理应用的能耗情况，并据此发现能效优化机会。Kepler与Telegraf的指标组合能为终端用户提供优化各类网络应用功耗的完整解决方案。

## 环境配置

![Kepler-Telegraf集成架构](../fig/Kepler-Telegraf.jpg)

### 控制平面服务器配置

| 组件          | 规格详情                     |
|---------------|----------------------------|
| 型号          | Intel(R) Xeon(R) Gold 6230N CPU @ 2.30GHz |
| 物理CPU数量   | 2                          |
| 单CPU核心数   | 20                         |
| 总逻辑核心数  | 80                         |
| 操作系统      | Ubuntu 22.04.1 LTS         |

### 下载安装Kepler

Kepler支持多种安装方式，具体步骤请参考[官方文档](https://sustainable-computing.io/installation/kepler/)：

```sh
root@: git clone https://github.com/sustainable-computing-io/kepler.git
root@: cd kepler/
root@: make build-manifest OPTS="BM_DEPLOY PROMETHEUS_DEPLOY"
root@: cd _output/generated-manifest/
root@: vi deployment.yaml
root@: kubectl apply -f _output/generated-manifest/deployment.yaml
```

通过以下命令验证安装：

```sh
root@: docker ps -a | grep 'kepler'

530a71f0067f        quay.io/sustainable_computing_io/kepler           "/bin/sh –
c '/usr/bi…"   33秒前       Up 31秒
k8s_kepler-exporter_kepler-exporter-bzj9b_kepler_827ee818-9f5a-460c-a368-
fc90fde5d378_0
decae0dc60e2        k8s.gcr.io/pause:3.3                              "/pause"
38秒前       Up 35秒
k8s_POD_kepler-exporter-bzj9b_kepler_827ee818-9f5a-460c-a368-fc90fde5d378_0

root@:~# kubectl get pod -n kepler
NAME                    READY   STATUS    RESTARTS   AGE
kepler-exporter-8h8x7   1/1     Running   0          63s
kepler-exporter-bzj9b   1/1     Running   0          63s
root@:~# kubectl port-forward kepler-exporter-jdklk 9102:9102 -n kepler --address='0.0.0.0'
```

### 下载运行Telegraf

Telegraf支持多种安装方式，本文采用源码编译方式：

系统要求：
- Go语言版本 ≥1.22（安装参考：[Go安装指南](https://golang.org/doc/install)）
- GNU make工具
- 满足Go语言[最低系统要求](https://go.dev/wiki/MinimumRequirements)

克隆仓库：
```sh
root@:~# git clone https://github.com/influxdata/telegraf.git
```

编译安装：
```sh
root@:~# cd telegraf
root@:~# make build
```

生成配置文件：
```sh
root@:~# telegraf config > telegraf.conf
```

编辑配置文件启用以下插件：

**输入插件：**
- [Intel PowerStat插件](https://github.com/influxdata/telegraf/tree/master/plugins/inputs/intel_powerstat)
- [Intel PMU插件](https://github.com/influxdata/telegraf/tree/master/plugins/inputs/intel_pmu)
- [IPMI传感器](https://github.com/influxdata/telegraf/tree/master/plugins/inputs/ipmi_sensor)

**输出插件：**
必须启用[Prometheus客户端输出插件](https://github.com/influxdata/telegraf/tree/master/plugins/outputs/prometheus_client)以存储指标到Prometheus

配置示例：
```sh
root@:~# vi telegraf.conf

[global_tags]
[agent]
  interval = "10s"
  round_interval = true
  metric_batch_size = 1000
  metric_buffer_limit = 10000
  collection_jitter = "0s"
  flush_interval = "10s"
  flush_jitter = "0s"

[[outputs.prometheus_client]]
  listen = ":9273"

[[inputs.intel_powerstat]]
  package_metrics = ["current_power_consumption", "current_dram_power_consumption", "thermal_design_power", "max_turbo_frequency", "uncore_frequency", "cpu_base_frequency"]
  cpu_metrics = ["cpu_frequency", "cpu_busy_frequency", "cpu_temperature", "cpu_c1_state_residency", "cpu_c6_state_residency", "cpu_busy_cycles"]

[[inputs.intel_pmu]]
  event_definitions = ["/root/.cache/pmu-events/GenuineIntel-6-55-7-core.json", "/root/.cache/pmu-events/GenuineIntel-6-55-7-uncore.json"]
  [[inputs.intel_pmu.core_events]]
    events = ["INST_RETIRED.ANY", "CPU_CLK_UNHALTED.THREAD_ANY:config1=0x4043200000000k"]
    cores = ["0"]
  [[inputs.intel_pmu.uncore_events]]
    events = ["UNC_CHA_CLOCKTICKS", "UNC_CHA_TOR_OCCUPANCY.IA_MISS"]
    sockets = ["0"]

[[inputs.ipmi_sensor]]
  use_sudo = true
  interval = "30s"
  timeout = "20s"
  metric_version = 2
```

启动Telegraf：
```sh
root@:~#./telegraf --config telegraf.conf
```

### 下载运行Prometheus容器

创建Prometheus配置文件，同时采集Kepler和Telegraf数据：

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'kepler'
    static_configs:
      - targets: ['xx.xx.xx:9102']
  - job_name: 'telegraf'
    static_configs:
      - targets: ['xx.xx.xx:9273']
```

启动容器：
```sh
root@:~# docker run -d -p 9090:9090 -v $PWD/prometheus.yaml:/etc/prometheus/prometheus.yml prom/prometheus
```

访问localhost:9090确认数据采集状态：

![Kepler-Telegraf-Prometheus监控](../fig/Kepler-Telegraf-Prometheus.png)

### 下载运行Grafana容器

启动Grafana：
```sh
root@:~# docker run -d --network host --name grafana grafana/grafana
```

访问localhost:3000，使用默认凭证登录后：
1. 添加Prometheus数据源
2. 导入[Kepler默认仪表盘](https://github.com/sustainable-computing-io/kepler/blob/main/grafana-dashboards/Kepler-Exporter.json)
3. 编辑仪表盘添加Telegraf指标

示例仪表盘：
- 左侧显示Kepler按命名空间统计的功耗指标
- 右侧显示Telegraf采集的电源指标

![集成仪表盘](../fig/Kepler-Telegraf-dashboard.png)

**指标说明：**

**Kepler指标：**
- **PKG->** `kepler_container_package_joules_total`：CPU封装总能耗（包含所有核心及非核心组件）
- **DRAM->** `kepler_container_dram_joules_total`：容器DRAM能耗
- **Other->** `kepler_container_other_joules_total`：除CPU/DRAM外其他主机组件能耗

**Telegraf指标：**
- **Total PKG current Power->** `powerstat_package_current_power_consumptions`：处理器封装当前功耗（双路总和）
- **Total DRAM power->** `powerstat_package_current_dram_power_consumptions`：DRAM总功耗
- **Total Thermal design Power->** `powerstat_package_current_thermal_power_consumptions`：处理器TDP设计功耗上限

**DRAM功耗指标在Kepler与Telegraf中的数值应基本吻合**

#### IPMI电源指标

仪表盘还可展示Telegraf通过IPMI采集的电源供应器电流输出百分比：

![IPMI电源指标](../fig/Kepler-Telegraf-IPMI.png)

## 参考文献

\[1\] <https://sustainable-computing.io/>

\[2\] <https://github.com/influxdata/telegraf>