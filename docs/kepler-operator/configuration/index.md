# PowerMonitor Configuration Guide

This guide covers comprehensive configuration options for the PowerMonitor Custom
Resource Definition (CRD). Use these settings to customize your Kepler deployment
for different environments, security requirements, and monitoring needs.

## Basic Configuration

### Metric Levels

Control which types of metrics Kepler exports. Choose based on your monitoring
requirements and performance considerations:

```yaml
spec:
  kepler:
    config:
      metricLevels:
      - node      # Node-level power consumption (recommended)
      - pod       # Pod-level power consumption (recommended)
      - vm        # Virtual machine power consumption
      - process   # Process-level power consumption (high overhead)
      - container # Container-level power consumption (high overhead)
```

**Recommendations:**

- **Production**: Use `node` and `pod` for balanced monitoring
- **Development**: Add `container` for detailed analysis
- **Minimal overhead**: Use `node` only

### Timing Configuration

Configure how frequently Kepler samples and reports metrics:

```yaml
spec:
  kepler:
    config:
      sampleRate: 5s      # How often to sample metrics
      staleness: 500ms    # How long before values are considered stale
```

**Performance tuning:**

- **Lower CPU usage**: Increase `sampleRate` to `10s` or `15s`
- **Higher precision**: Decrease `sampleRate` to `3s` (minimum recommended)
- **Network optimization**: Adjust `staleness` based on network latency

### Logging Configuration

Set logging levels for troubleshooting and monitoring:

```yaml
spec:
  kepler:
    config:
      logLevel: info  # Options: debug, info, warn, error
```

**Log levels:**

- **`debug`**: Verbose logging for troubleshooting (not for production)
- **`info`**: Standard operational logging (recommended)
- **`warn`**: Only warnings and errors
- **`error`**: Only error messages

## Resource Management

### Terminated Workload Tracking

Control how Kepler handles metrics for terminated pods and containers:

```yaml
spec:
  kepler:
    config:
      maxTerminated: 500  # Track top 500 terminated workloads by power consumption
```

**Options:**

- **`500`** (default): Track top 500 terminated workloads
- **`0`**: Disable terminated workload tracking (saves memory)
- **`-1`**: Track unlimited terminated workloads (use with caution)

### Additional ConfigMaps

Use external ConfigMaps for advanced configuration:

```yaml
spec:
  kepler:
    config:
      additionalConfigMaps:
      - name: custom-model-config
      - name: advanced-power-settings
```

This allows you to:

- Override power models
- Customize CPU frequency mappings
- Configure platform-specific settings

## Security Configuration

### RBAC Mode

Configure security and service account permissions:

```yaml
spec:
  kepler:
    deployment:
      security:
        mode: rbac              # Options: none, rbac
        allowedSANames:
        - "monitoring-sa"
        - "custom-service-account"
```

**Security modes:**

- **`none`**: No additional security restrictions (default for development)
- **`rbac`**: Enable Role-Based Access Control (recommended for production)

### Service Account Configuration

When using RBAC mode, specify allowed service accounts:

```yaml
spec:
  kepler:
    deployment:
      security:
        mode: rbac
        allowedSANames:
        - "prometheus-service-account"
        - "grafana-service-account"
```

## Node Selection and Scheduling

### Node Selectors

Control which nodes run Kepler pods:

```yaml
spec:
  kepler:
    deployment:
      nodeSelector:
        kubernetes.io/os: linux
        node-type: worker
        monitoring: enabled
```

Common selectors:

- **OS selection**: `kubernetes.io/os: linux`
- **Node roles**: `node-role.kubernetes.io/worker: ""`
- **Custom labels**: `monitoring: enabled`

### Tolerations

Allow Kepler to run on nodes with specific taints:

```yaml
spec:
  kepler:
    deployment:
      tolerations:
      - key: node-role.kubernetes.io/master
        operator: Exists
        effect: NoSchedule
      - key: dedicated
        operator: Equal
        value: monitoring
        effect: NoSchedule
```

**Common tolerations:**

- **Master nodes**: Allow monitoring on control plane nodes
- **Dedicated nodes**: Run on nodes dedicated to monitoring
- **Special hardware**: Nodes with specific hardware requirements

## Complete Configuration Examples

### Development Environment

```yaml
apiVersion: kepler.system.sustainable.computing.io/v1alpha1
kind: PowerMonitor
metadata:
  name: power-monitor-dev
spec:
  kepler:
    config:
      logLevel: debug
      metricLevels:
      - node
      - pod
      - container
      sampleRate: 3s
      staleness: 200ms
      maxTerminated: 100
    deployment:
      security:
        mode: none
```

### Production Environment

```yaml
apiVersion: kepler.system.sustainable.computing.io/v1alpha1
kind: PowerMonitor
metadata:
  name: power-monitor-prod
spec:
  kepler:
    config:
      logLevel: warn
      metricLevels:
      - node
      - pod
      sampleRate: 10s
      staleness: 1s
      maxTerminated: 1000
    deployment:
      security:
        mode: rbac
        allowedSANames:
        - "prometheus-operator-prometheus"
      nodeSelector:
        kubernetes.io/os: linux
        node-role.kubernetes.io/worker: ""
      tolerations:
      - key: dedicated
        operator: Equal
        value: monitoring
        effect: NoSchedule
```

### High-Performance Monitoring

```yaml
apiVersion: kepler.system.sustainable.computing.io/v1alpha1
kind: PowerMonitor
metadata:
  name: power-monitor-hpc
spec:
  kepler:
    config:
      logLevel: info
      metricLevels:
      - node
      - pod
      - vm
      - process
      sampleRate: 1s
      staleness: 100ms
      maxTerminated: -1  # Track all terminated workloads
      additionalConfigMaps:
      - name: hpc-power-models
    deployment:
      security:
        mode: rbac
      nodeSelector:
        node-type: compute-intensive
      tolerations:
      - key: high-performance
        operator: Exists
        effect: NoSchedule
```

## Configuration Validation

### Check Configuration

Verify your PowerMonitor configuration:

```bash
# Check PowerMonitor status
oc get powermonitor power-monitor -o yaml

# Verify conditions
oc describe powermonitor power-monitor

# Check generated resources
oc get all -n power-monitor
```

### Common Configuration Issues

**Issue**: Pods not scheduling on intended nodes

```bash
# Check node labels
oc get nodes --show-labels

# Update nodeSelector
oc patch powermonitor power-monitor --type='merge' -p='
{
  "spec": {
    "kepler": {
      "deployment": {
        "nodeSelector": {
          "kubernetes.io/os": "linux"
        }
      }
    }
  }
}'
```

**Issue**: High resource usage

```bash
# Reduce metric levels and increase sample rate
oc patch powermonitor power-monitor --type='merge' -p='
{
  "spec": {
    "kepler": {
      "config": {
        "metricLevels": ["node", "pod"],
        "sampleRate": "10s"
      }
    }
  }
}'
```

## Advanced Topics

For more advanced configuration scenarios, see:

- **[Monitoring & Troubleshooting](monitoring-troubleshooting.md)** - Advanced monitoring setup
- **[Migration Guide](../migration/index.md)** - Migrating from legacy configurations
