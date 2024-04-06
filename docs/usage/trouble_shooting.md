# Trouble Shooting

## Kepler Pod failed to start

### Background

Kepler uses eBPF to obtain performance counter readings and processes stats. Since eBPF requires kernel
headers, Kepler will fail to start up when the kernel headers are missing.

### Diagnose

To confirm, check the Kepler Pod logs with the following command and look for message
`not able to load eBPF modules`.

```bash
kubectl logs -n kepler daemonset/kepler-exporter
```

### Solution

Installing kernel headers on each node can be done manually using the following command

```bash
# Fedora/RHEL based distro
dnf install kernel-devel-`uname -r` -y
# Debian/Ubuntu distro
apt install linux-headers-$(uname -r)
```

On OpenShift, install the MachineConfiguration [here](https://github.com/sustainable-computing-io/kepler/tree/main/manifests/config/cluster-prereqs)

## Kepler energy metrics are zeroes

<!-- markdownlint-disable MD024 -->
### Background

Kepler uses RAPL counters on x86 platforms to read energy consumption.
VMs do not have RAPL counters and thus Kepler estimates energy consumption based on the pre-trained
ML models. The models use either hardware performance counters or cGroup stats to estimate energy
consumed by processes. Currently the cGroup based models use cGroup v2 features such as
`cgroupfs_cpu_usage_us`, `cgroupfs_memory_usage_bytes`, `cgroupfs_system_cpu_usage_us`,
`cgroupfs_user_cpu_usage_us`, `bytes_read`, and `bytes_writes`.

### Diagnose

The Kepler metrics are zeroes, check if cGroup version on the node:

```bash
ls /sys/fs/cgroup/cgroup.controllers
```

### Solution
<!-- markdownlint-enable MD024 -->

Enable cGroup v2 on the node by following [these Kubernetes instruction](https://kubernetes.io/docs/concepts/architecture/cgroups/).

On OpenShift, apply [these cGroup v2 MachineConfiguration](https://github.com/sustainable-computing-io/kepler/tree/main/manifests/config/cluster-prereqs)
