# Kepler Model Server Compatibility Notice

⚠️ **COMPATIBILITY WARNING** ⚠️

## Model Server Status with Kepler v0.10.0+

The **Kepler Model Server is NOT compatible** with Kepler v0.10.0 and above due
to the major architectural rewrite. The Model Server documentation in this
section applies **only to Kepler v0.9.0 and below**.

## What Changed in v0.10.0

Kepler v0.10.0 introduced fundamental changes that break Model Server compatibility:

### Metrics Structure Changes

- **Old**: Complex component-based metrics (core, uncore, package, DRAM, GPU)
- **New**: Simplified CPU-focused metrics with zone-based organization
- **Impact**: Model Server expects the old metric names and structure

### Power Attribution Changes

- **Old**: Hardware counter-based attribution with detailed component breakdown
- **New**: CPU-time-proportional attribution with active/idle split
- **Impact**: Model training data format and attribution logic incompatible

### Configuration System Changes

- **Old**: Environment variable-based configuration that Model Server integrated with
- **New**: CLI flags + YAML hierarchy with different configuration structure
- **Impact**: Model Server configuration integration no longer works

## Current Status

🔴 **Not Working**: Model Server integration with Kepler v0.10.0+

🟡 **Under Review**: Compatibility assessment and potential updates

🔵 **Future Plans**: Model Server updates may be planned for future releases

## For Legacy Users

If you need to use the Model Server:

1. **Use Kepler v0.9.0 or below** with the legacy architecture
2. **Refer to archived documentation** for proper setup procedures
3. **See the [Archive section](archive/README.md)** for legacy installation guides

## Alternative Solutions

For Kepler v0.10.0+ users needing power modeling:

1. **Direct Metrics Export**: Use the simplified metrics directly for analysis
2. **Custom Integration**: Build custom solutions using the new metric structure
3. **Wait for Updates**: Monitor the project for Model Server compatibility updates

## Stay Updated

- **GitHub Issues**: Watch for Model Server compatibility updates
- **Community Discussions**: Join discussions about Model Server future
- **Release Notes**: Check future release notes for compatibility announcements

---

⚠️ **Do not attempt to use Model Server documentation with Kepler v0.10.0+**
as it will result in configuration errors and incompatible integrations.
