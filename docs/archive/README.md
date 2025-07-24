# Archived Documentation - Kepler v0.9.0 and Below

⚠️ **DEPRECATED DOCUMENTATION** ⚠️

This directory contains documentation for Kepler versions 0.9.0 and below.
This documentation is **outdated** and applies to the legacy eBPF-based
architecture that was replaced in Kepler v0.10.0+.

## What Changed in v0.10.0+

Kepler underwent a major architectural rewrite in v0.10.0 that introduced:

- **Service-oriented design** replacing eBPF-centric architecture
- **Simplified configuration** with CLI flags + YAML instead of 40+ environment variables
- **Streamlined metrics** with CPU-focused attribution instead of complex component breakdowns
- **New development workflow** with Docker Compose environments

## Using This Documentation

**DO NOT use this documentation for Kepler v0.10.0+.** It will lead to:

- Incorrect configuration attempts
- Wrong metric names and structures
- Outdated installation procedures
- Obsolete troubleshooting steps

## For Current Documentation

Please refer to the main documentation sections for up-to-date information:

- `/docs/design/` - Current architecture and design
- `/docs/installation/` - Current installation methods
- `/docs/usage/` - Current configuration and usage
