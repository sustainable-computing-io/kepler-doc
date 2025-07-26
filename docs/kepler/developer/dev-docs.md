# Developer Documentation

## 📍 Location of Developer Documentation

Developer documentation for Kepler and related projects is maintained within
each project's repository under the `docs/developer/` directory.

## 🔗 Kepler Developer Documentation

For comprehensive developer documentation including architecture, development
workflows, testing strategies, and contribution guidelines, please visit:

**🚀 [Kepler Developer Documentation](https://github.com/sustainable-computing-io/kepler/tree/main/docs/developer)**

### What You'll Find There

- **Architecture Overview** - Service-oriented design patterns and component structure
- **Development Environment Setup** - Docker Compose, local builds, and testing
- **Power Attribution Guide** - Deep dive into energy measurement and attribution algorithms
- **Pre-commit Hooks** - Code quality and automated checks setup
- **Release Workflow** - How releases are created and managed
- **Testing Strategy** - Unit tests, integration tests, and race detection
- **Service Interfaces** - Understanding the service framework and lifecycle management
- **Configuration Management** - YAML hierarchy and CLI flag systems

## 🛠️ Quick Developer Setup

For immediate development setup, the key commands are:

```bash
# Clone and build
git clone https://github.com/sustainable-computing-io/kepler.git
cd kepler
make build

# Development with Docker Compose (includes Grafana + Prometheus)
cd compose/dev
docker-compose up -d

# Run tests
make test

# Local development
sudo ./bin/kepler --config hack/config.yaml
```

## 📚 Related Project Documentation

For other projects in the Kepler ecosystem, check their respective repositories:

- **Kepler Operator**: [sustainable-computing-io/kepler-operator](https://github.com/sustainable-computing-io/kepler-operator)
- **Kepler Model Server**: [sustainable-computing-io/kepler-model-server](https://github.com/sustainable-computing-io/kepler-model-server)

## 🤝 Contributing

Before contributing to Kepler, please review:

1. **[Developer Documentation](https://github.com/sustainable-computing-io/kepler/tree/main/docs/developer)** - Technical implementation details
2. **[Contributing Guide](../../project/contributing.md)** - General contribution process
3. **[Code of Conduct](https://github.com/sustainable-computing-io/kepler/blob/main/CODE_OF_CONDUCT.md)** - Community guidelines

## 💬 Developer Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/sustainable-computing-io/kepler/issues)
- **GitHub Discussions**: [Ask questions and share ideas](https://github.com/sustainable-computing-io/kepler/discussions)
- **Slack Channel**: [#kepler in CNCF Slack](https://cloud-native.slack.com/archives/C06HYDN4A01)

---

*Developer documentation is actively maintained in the project repository to ensure it stays current with the codebase.*
