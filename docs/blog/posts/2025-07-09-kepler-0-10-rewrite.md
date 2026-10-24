---
date: 2025-07-09
slug: kepler-0-10-rewrite
---

# Kepler 0.10.0: A Ground-Up Rewrite

**Important Notice:** Starting with version 0.10.0, Kepler has undergone a complete ground-up rewrite.
This represents a significant architectural improvement while maintaining the core mission of
accurate energy consumption monitoring for cloud-native workloads.

> 📢 **Read the full announcement:** [CNCF Slack Announcement](https://cloud-native.slack.com/archives/C05QK3KN3HT/p1752049660866519)

<!-- more -->

## ✨ What's New in the Rewrite

**Enhanced Performance & Accuracy:**

- Dynamic detection of Nodes' RAPL zones - no more hardcoded RAPL zones
- More accurate power attribution based on active CPU usage (no more idle/dynamic for workloads)
- Improved VM, Container, and Pod detection with more meaningful label values
- Significantly reduced resource usage compared to old Kepler

**Reduced Security Requirements:**

- Requires only readonly access to host `/proc` and `/sys`
- No more `CAP_SYSADMIN` or `CAP_BPF` capabilities required
- Much fewer privileges than previous versions

**Modern Architecture:**

- Service-oriented design with clean separation of concerns
- Thread-safe operations throughout the codebase
- Graceful shutdown handling with proper resource cleanup
- Comprehensive error handling with structured logging

**Current Limitations:**

- Supports RAPL/powercap framework, with experimental support for HWMon, GPU (NVIDIA), and platform power (Redfish BMC)

## 📚 Migration & Legacy Support

**For New Users:** Use the current version (0.10.0+) for the best experience and latest features.

**For Existing Users:** If you need to continue using the old version:

- Pin your deployment to version `0.9.0` (final legacy release)
- Access the old codebase in the [archived branch](https://github.com/sustainable-computing-io/kepler/tree/archived)
- **Important:** The legacy version (0.9.x and earlier) is now frozen - no bug fixes or feature requests will be accepted for the old version

**Migration Note:** Please review the new configuration format and deployment methods in the [Installation Guide](../../kepler/installation/guide.md) and [Configuration Guide](../../kepler/usage/configuration.md) when upgrading to 0.10.0+.
