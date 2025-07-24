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
