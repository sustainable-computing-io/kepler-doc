# PowerMonitor Operator on OpenShift

## Overview

The Kepler Operator provides a streamlined way to deploy and manage Kepler (Kubernetes
Efficient Power Level Exporter) on OpenShift clusters. The operator uses the modern
PowerMonitor Custom Resource Definition to provide enhanced configuration options and
improved resource management.

## Migration Notice

!!! warning "Important"
    The Kepler CRD is deprecated and will be removed in a future release. Please
    use PowerMonitor instead for all new deployments and migrate existing
    installations to ensure continued support.

## Prerequisites

Before installing the Kepler Operator, ensure you have:

- OpenShift cluster access with `cluster-admin` privileges
- User Workload Monitoring enabled in your cluster
- Access to OperatorHub (for UI installation)
- `oc` CLI tool installed (for command-line operations)

!!! note
    Your operator will automatically use the current context in your kubeconfig
    file (i.e. whatever cluster `oc cluster-info` shows).

## Installation Options

Choose the installation method that best fits your workflow:

### [Quick Start Guide](quickstart.md) (Recommended)

Best for users new to the Kepler Operator who want to get up and running quickly
using the OpenShift web console.

- Install via OperatorHub
- Create basic PowerMonitor instance
- Verify installation
- Access initial metrics

### [CLI Installation Guide](cli-installation.md)

Perfect for automation, scripting, or users who prefer command-line workflows.

- Install operator via command line
- Deploy PowerMonitor using YAML
- Verification commands
- Scripting examples

## Post-Installation

Once you have the operator installed, explore these guides:

### [Configuration Guide](../configuration/index.md)

Learn how to customize your Kepler deployment:

- Metric levels and sampling rates
- Security configurations
- Resource management
- Node selection and tolerations
- Advanced configuration options

### [Monitoring & Troubleshooting](../configuration/monitoring-troubleshooting.md)

Set up monitoring and resolve common issues:

- User Workload Monitoring setup
- OpenShift metrics dashboard
- Grafana integration
- Common troubleshooting scenarios

## Migration

### [Migration Guide](../migration/index.md)

If you're upgrading from the deprecated Kepler CRD:

- Step-by-step migration process
- Configuration comparison
- Rollback procedures

## Getting Help

- [Project Resources](../../project/resources.md) - Additional documentation and resources
- [Support](../../project/support.md) - Community support and contribution guidelines
