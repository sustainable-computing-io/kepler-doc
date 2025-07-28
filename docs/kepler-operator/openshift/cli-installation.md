# CLI Installation Guide

This guide shows how to install the Kepler Operator and create PowerMonitor instances
using the OpenShift command-line interface. This approach is ideal for automation,
scripting, and users who prefer terminal-based workflows.

## Prerequisites

Ensure you have:

- `oc` CLI tool installed and configured
- Cluster admin privileges on your OpenShift cluster
- Current context pointing to target cluster (`oc cluster-info`)

## Step 1: Install the Operator

### Create Operator Subscription

Install the Kepler Operator from the community catalog:

```bash
oc apply -f - << EOF
apiVersion: operators.coreos.com/v1alpha1
kind: Subscription
metadata:
  name: kepler-operator
  namespace: openshift-operators
spec:
  channel: alpha
  name: kepler-operator
  source: community-operators
  sourceNamespace: openshift-marketplace
EOF
```

### Verify Installation

Wait for the operator to be ready:

```bash
# Check subscription status
oc get subscription kepler-operator -n openshift-operators

# Check ClusterServiceVersion (CSV)
oc get csv -n openshift-operators | grep kepler

# Wait for operator pod to be running
oc get pods -n openshift-operators | grep kepler-operator
```

Expected output when ready:

```text
kepler-operator-controller-manager-xxx   2/2     Running   0   2m
```

## Step 2: Create PowerMonitor Instance

### Basic PowerMonitor Configuration

Create a PowerMonitor with default settings:

```bash
oc apply -f - << EOF
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
      staleness: 500ms
      maxTerminated: 500
    deployment:
      security:
        mode: none
EOF
```

### Verify PowerMonitor Deployment

Check that the PowerMonitor was created and is operational:

```bash
# Check PowerMonitor status
oc get powermonitor power-monitor -o wide

# Check conditions
oc describe powermonitor power-monitor

# Verify DaemonSet creation
oc get daemonset -n power-monitor

# Check pods on all nodes
oc get pods -n power-monitor -o wide
```

## Step 3: Verification Commands

### Check Operator Health

```bash
# Operator pod status
oc get pods -n openshift-operators | grep kepler-operator

# Operator logs
oc logs -n openshift-operators deployment/kepler-operator-controller-manager
```

### Check PowerMonitor Resources

```bash
# PowerMonitor status and conditions
oc get powermonitor power-monitor -o yaml

# DaemonSet details
oc describe daemonset -n power-monitor

# Pod logs
oc logs -n power-monitor -l app.kubernetes.io/name=kepler-exporter
```

### Test Metrics Endpoint

```bash
# Port forward to metrics endpoint
oc port-forward -n power-monitor svc/kepler-exporter 9102:9102 &

# Test metrics (in another terminal)
curl http://localhost:9102/metrics | head -20

# Stop port forwarding
pkill -f "port-forward.*9102"
```

## Automation Scripts

### Complete Installation Script

Save this as `install-kepler-operator.sh`:

```bash
#!/bin/bash
set -e

echo "Installing Kepler Operator..."

# Install operator
oc apply -f - << EOF
apiVersion: operators.coreos.com/v1alpha1
kind: Subscription
metadata:
  name: kepler-operator
  namespace: openshift-operators
spec:
  channel: alpha
  name: kepler-operator
  source: community-operators
  sourceNamespace: openshift-marketplace
EOF

echo "Waiting for operator to be ready..."
while ! oc get csv -n openshift-operators | grep -q kepler.*Succeeded; do
  echo "Waiting for CSV to be ready..."
  sleep 10
done

echo "Creating PowerMonitor instance..."
oc apply -f - << EOF
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
      security:
        mode: none
EOF

echo "Waiting for DaemonSet to be ready..."
while ! oc get daemonset -n power-monitor 2>/dev/null | grep -q kepler; do
  echo "Waiting for DaemonSet creation..."
  sleep 5
done

echo "Installation complete!"
echo "Check status with: oc get powermonitor power-monitor"
```

Make it executable and run:

```bash
chmod +x install-kepler-operator.sh
./install-kepler-operator.sh
```

### Uninstall Script

Save this as `uninstall-kepler-operator.sh`:

```bash
#!/bin/bash
set -e

echo "Removing PowerMonitor instance..."
oc delete powermonitor power-monitor --ignore-not-found=true

echo "Waiting for resources cleanup..."
sleep 10

echo "Removing operator subscription..."
oc delete subscription kepler-operator -n openshift-operators --ignore-not-found=true

echo "Removing CSV..."
oc delete csv -n openshift-operators $(oc get csv -n openshift-operators -o name | grep kepler) --ignore-not-found=true

echo "Uninstall complete!"
```

## Configuration Files

For production deployments, save configurations to files:

### powermonitor-basic.yaml

```yaml
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
```

### powermonitor-production.yaml

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
      staleness: 1s
      maxTerminated: 1000
    deployment:
      security:
        mode: rbac
      nodeSelector:
        kubernetes.io/os: linux
      tolerations:
      - key: node-role.kubernetes.io/master
        operator: Exists
        effect: NoSchedule
```

Apply with:

```bash
oc apply -f powermonitor-production.yaml
```

## Next Steps

- **[Configuration Guide](../configuration/index.md)** - Advanced configuration options
- **[Monitoring Setup](../configuration/monitoring-troubleshooting.md)** - Set up monitoring and troubleshooting
