# Migration Guide: Kepler CRD to PowerMonitor

This guide helps you migrate from the deprecated Kepler CRD to the modern
PowerMonitor CRD. The PowerMonitor provides enhanced configuration options,
improved resource management, and better OpenShift integration.

## Migration Overview

### Why Migrate?

!!! warning "Deprecation Notice"
    The Kepler CRD is deprecated and will be removed in a future release.
    Migrate to PowerMonitor to ensure continued support and access to new features.

**Benefits of PowerMonitor:**

- Enhanced security configurations
- Improved resource management
- Better OpenShift integration
- More granular metric control
- Active development and support

### Migration Impact

**Zero-downtime migration:** The migration process allows you to run both CRDs
simultaneously during the transition, ensuring continuous monitoring.

**Configuration differences:** Some configuration options have changed or been
reorganized. This guide provides mapping between old and new configurations.

## Pre-Migration Assessment

### Step 1: Inventory Current Deployment

Document your existing Kepler CRD configuration:

```bash
# List existing Kepler resources
oc get kepler --all-namespaces

# Export current configuration
oc get kepler kepler -o yaml > kepler-backup.yaml

# Save current DaemonSet configuration for reference
oc get daemonset -n kepler -o yaml > kepler-daemonset-backup.yaml
```

### Step 2: Review Configuration Mapping

Common configuration changes:

| Kepler CRD (Old) | PowerMonitor CRD (New) |
|-------------------|------------------------|
| `spec.exporter.deployment.port` | Managed automatically |
| `spec.exporter.config.logLevel` | `spec.kepler.config.logLevel` |
| `spec.nodeSelector` | `spec.kepler.deployment.nodeSelector` |
| `spec.tolerations` | `spec.kepler.deployment.tolerations` |

## Migration Process

### Step 1: Create Equivalent PowerMonitor

#### Example Migration: Basic Configuration

**Old Kepler CRD:**

```yaml
apiVersion: kepler.system.sustainable.computing.io/v1alpha1
kind: Kepler
metadata:
  name: kepler
spec:
  exporter:
    deployment:
      port: 9102
    config:
      logLevel: info
  nodeSelector:
    kubernetes.io/os: linux
```

**New PowerMonitor CRD:**

```yaml
apiVersion: kepler.system.sustainable.computing.io/v1alpha1
kind: PowerMonitor
metadata:
  name: power-monitor
  labels:
    app.kubernetes.io/name: powermonitor
    app.kubernetes.io/instance: powermonitor
    app.kubernetes.io/part-of: kepler-operator
spec:
  kepler:
    config:
      logLevel: info
      metricLevels:
      - node
      - pod
      - vm
      sampleRate: 5s
    deployment:
      nodeSelector:
        kubernetes.io/os: linux
      security:
        mode: none
```

#### Example Migration: Advanced Configuration

**Old Kepler CRD:**

```yaml
apiVersion: kepler.system.sustainable.computing.io/v1alpha1
kind: Kepler
metadata:
  name: kepler
spec:
  exporter:
    config:
      logLevel: warn
  nodeSelector:
    node-role.kubernetes.io/worker: ""
  tolerations:
  - key: node-role.kubernetes.io/master
    operator: Exists
    effect: NoSchedule
```

**New PowerMonitor CRD:**

```yaml
apiVersion: kepler.system.sustainable.computing.io/v1alpha1
kind: PowerMonitor
metadata:
  name: power-monitor
spec:
  kepler:
    config:
      logLevel: warn
      metricLevels: [node, pod]
      sampleRate: 10s
      maxTerminated: 500
    deployment:
      nodeSelector:
        node-role.kubernetes.io/worker: ""
      tolerations:
      - key: node-role.kubernetes.io/master
        operator: Exists
        effect: NoSchedule
      security:
        mode: rbac
```

### Step 2: Deploy PowerMonitor Alongside Existing Kepler

Deploy the PowerMonitor while keeping the old Kepler CRD running:

```bash
# Create PowerMonitor configuration
cat > power-monitor.yaml << EOF
apiVersion: kepler.system.sustainable.computing.io/v1alpha1
kind: PowerMonitor
metadata:
  name: power-monitor
spec:
  kepler:
    config:
      logLevel: info
      metricLevels: [node, pod, vm]
      sampleRate: 5s
    deployment:
      security:
        mode: none
EOF

# Apply PowerMonitor
oc apply -f power-monitor.yaml
```

### Step 3: Verify PowerMonitor Functionality

Ensure the PowerMonitor is working correctly:

```bash
# Check PowerMonitor status
oc get powermonitor power-monitor -o wide

# Verify DaemonSet creation
oc get daemonset -n power-monitor

# Check pods are running
oc get pods -n power-monitor

# Test metrics endpoint
oc port-forward -n power-monitor svc/kepler-exporter 9103:9102 &
curl http://localhost:9103/metrics | head -10
```

### Step 4: Update Monitoring Configuration

If you have existing monitoring setup, update it to use the new PowerMonitor:

#### Prometheus ServiceMonitor

Update or create ServiceMonitor for the new namespace:

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: kepler-exporter
  namespace: power-monitor
spec:
  selector:
    matchLabels:
      app.kubernetes.io/name: kepler-exporter
  endpoints:
  - port: http
    path: /metrics
```

#### Grafana Dashboard

Update Grafana queries to use the new service:

```promql
# Update queries from:
{__name__=~"kepler_.*", job="kepler"}

# To:
{__name__=~"kepler_.*", job="kepler-exporter", namespace="power-monitor"}
```

### Step 5: Remove Old Kepler CRD

After verifying the PowerMonitor works correctly:

```bash
# Remove old Kepler resource
oc delete kepler kepler

# Clean up old namespace (if different)
oc delete namespace kepler

# Verify cleanup
oc get kepler --all-namespaces
```

## Configuration Migration Reference

### Complete Mapping Table

| Old Configuration | New Configuration | Notes |
|------------------|-------------------|-------|
| `spec.exporter.config.logLevel` | `spec.kepler.config.logLevel` | Same values |
| `spec.exporter.deployment.port` | Auto-managed | Port 9102 by default |
| `spec.nodeSelector` | `spec.kepler.deployment.nodeSelector` | Same format |
| `spec.tolerations` | `spec.kepler.deployment.tolerations` | Same format |
| N/A | `spec.kepler.config.metricLevels` | New: control metric granularity |
| N/A | `spec.kepler.config.sampleRate` | New: control sampling frequency |
| N/A | `spec.kepler.deployment.security` | New: RBAC and security options |
| N/A | `spec.kepler.config.maxTerminated` | New: control terminated workload tracking |

### Migration Script

Automate the migration with this script:

```bash
#!/bin/bash
# migrate-kepler-to-powermonitor.sh

set -e

KEPLER_NAME="${1:-kepler}"
POWERMONITOR_NAME="${2:-power-monitor}"

echo "Migrating Kepler CRD '${KEPLER_NAME}' to PowerMonitor '${POWERMONITOR_NAME}'"

# Export current Kepler configuration
echo "Exporting current Kepler configuration..."
oc get kepler ${KEPLER_NAME} -o yaml > kepler-backup-$(date +%Y%m%d-%H%M%S).yaml

# Extract configuration values
LOG_LEVEL=$(oc get kepler ${KEPLER_NAME} -o jsonpath='{.spec.exporter.config.logLevel}' 2>/dev/null || echo "info")
NODE_SELECTOR=$(oc get kepler ${KEPLER_NAME} -o jsonpath='{.spec.nodeSelector}' 2>/dev/null || echo "{}")
TOLERATIONS=$(oc get kepler ${KEPLER_NAME} -o jsonpath='{.spec.tolerations}' 2>/dev/null || echo "[]")

echo "Creating PowerMonitor with equivalent configuration..."

# Create PowerMonitor
cat > powermonitor-migration.yaml << EOF
apiVersion: kepler.system.sustainable.computing.io/v1alpha1
kind: PowerMonitor
metadata:
  name: ${POWERMONITOR_NAME}
  labels:
    app.kubernetes.io/name: powermonitor
    app.kubernetes.io/instance: powermonitor
    app.kubernetes.io/part-of: kepler-operator
    migrated-from: kepler-crd
spec:
  kepler:
    config:
      logLevel: ${LOG_LEVEL}
      metricLevels: [node, pod, vm]
      sampleRate: 5s
      maxTerminated: 500
    deployment:
      security:
        mode: none
EOF

# Add nodeSelector if it exists
if [ "${NODE_SELECTOR}" != "{}" ]; then
  echo "      nodeSelector:" >> powermonitor-migration.yaml
  echo "${NODE_SELECTOR}" | sed 's/^/        /' >> powermonitor-migration.yaml
fi

# Add tolerations if they exist
if [ "${TOLERATIONS}" != "[]" ]; then
  echo "      tolerations:" >> powermonitor-migration.yaml
  echo "${TOLERATIONS}" | sed 's/^/      /' >> powermonitor-migration.yaml
fi

# Apply PowerMonitor
oc apply -f powermonitor-migration.yaml

echo "Waiting for PowerMonitor to be ready..."
sleep 10

# Verify PowerMonitor
if oc get powermonitor ${POWERMONITOR_NAME} &>/dev/null; then
  echo "PowerMonitor created successfully!"
  echo "Verifying DaemonSet..."

  # Wait for DaemonSet
  timeout 60s bash -c "while ! oc get daemonset -n power-monitor | grep -q kepler; do sleep 2; done"

  echo "Migration complete!"
  echo "Run the following commands to verify:"
  echo "  oc get powermonitor ${POWERMONITOR_NAME}"
  echo "  oc get pods -n power-monitor"
  echo ""
  echo "After verification, remove the old Kepler CRD:"
  echo "  oc delete kepler ${KEPLER_NAME}"
else
  echo "Migration failed. Check the PowerMonitor configuration."
  exit 1
fi
```

Usage:

```bash
chmod +x migrate-kepler-to-powermonitor.sh
./migrate-kepler-to-powermonitor.sh [kepler-name] [powermonitor-name]
```

## Rollback Procedure

If you need to rollback to the Kepler CRD:

### Step 1: Recreate Kepler CRD

```bash
# Apply your backed-up Kepler configuration
oc apply -f kepler-backup.yaml
```

### Step 2: Remove PowerMonitor

```bash
# Remove PowerMonitor
oc delete powermonitor power-monitor

# Clean up namespace
oc delete namespace power-monitor
```

### Step 3: Verify Kepler CRD

```bash
# Check Kepler status
oc get kepler kepler
oc get pods -n kepler
```

## Post-Migration Tasks

### Update Documentation

- Update internal documentation to reference PowerMonitor
- Update automation scripts and CI/CD pipelines
- Train team members on new configuration options

### Monitoring Integration

- Update alerting rules for new namespace and service names
- Verify metrics collection in monitoring systems
- Update dashboards with new service discovery

### Cleanup

- Remove backup files after successful migration
- Clean up old monitoring configurations
- Update Infrastructure as Code (IaC) templates

## Getting Help

If you encounter issues during migration:

1. **Check logs**: Use the diagnostic commands in the [Troubleshooting Guide](../configuration/monitoring-troubleshooting.md)
2. **Community support**: See [Support](../../project/support.md) for community channels
3. **Report issues**: Create an issue in the [Kepler Operator repository](https://github.com/sustainable-computing-io/kepler-operator/issues)
