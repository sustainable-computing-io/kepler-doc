---
date: 2026-11-12
slug: kepler-operator-0-25-0
---

# Kepler Operator 0.25.0: Kepler 0.12 and a Helm fix

**Author:** Granite Tait

Kepler Operator 0.25.0 is out. It deploys Kepler 0.12.0, fixes a Helm chart bug that kept
installing an old operator, patches two CVEs, and adds the full user docs to the operator
repository. It is also live in the OpenShift Community Operators catalog.

> **Release notes:** [kepler-operator v0.25.0 on GitHub](https://github.com/sustainable-computing-io/kepler-operator/releases/tag/v0.25.0)

<!-- more -->

## Highlights

- **Kepler 0.12.0** is deployed by default, up from 0.11.4 ([#694](https://github.com/sustainable-computing-io/kepler-operator/pull/694))
- **Helm installs get the operator version they ask for.** Charts 0.23.0 and 0.24.0 deployed operator 0.21.0 ([#699](https://github.com/sustainable-computing-io/kepler-operator/pull/699))
- **Security fix** for CVE-2026-24051 and CVE-2026-29181 in the OpenTelemetry SDK ([#673](https://github.com/sustainable-computing-io/kepler-operator/pull/673))
- **Full user docs in the operator repository** ([#698](https://github.com/sustainable-computing-io/kepler-operator/pull/698))
- **One upgrade note:** if you set `experimental.hwmon.enabled`, read the [upgrade note](#upgrade-note-experimentalhwmonenabled-is-gone) before you upgrade

## The Helm chart was installing operator 0.21.0

The release workflow updated the chart version on each release but left `operator.image` behind.
Charts 0.23.0 and 0.24.0 both pointed at operator `0.21.0`. If you installed with Helm in that
window, you were running 0.21.0. You also missed the 0.24.0 change that swapped `privileged` for
`CAP_SYS_PTRACE` on the Kepler pods ([#651](https://github.com/sustainable-computing-io/kepler-operator/pull/651)).

Chart 0.25.0 deploys operator 0.25.0. The release workflow now bumps the image together with the chart,
and a validation script checks that they match.

Check which operator you are running:

```bash
kubectl get deploy -n kepler-operator -o jsonpath='{.items[*].spec.template.spec.containers[*].image}'
```

## Kepler 0.12.0 and two new ConfigMap options

The operator now deploys Kepler 0.12.0 and passes through its new settings via
[additional ConfigMaps](https://github.com/sustainable-computing-io/kepler-operator/blob/v0.25.0/docs/user/reference/custom-configmaps.md).

**Choosing CPU power meters.** `cpu.preferredMeters` lists backends in order. Kepler uses the
first one that starts and reports zones. The default is `[rapl, hwmon]`, so machines without RAPL
fall back to HWMON:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: kepler-cpu-config
  namespace: power-monitor
data:
  config.yaml: |
    cpu:
      preferredMeters:
        - rapl
        - hwmon
```

**Pointing at a DCGM exporter (experimental).** For NVIDIA MIG power attribution, you can set the
DCGM exporter endpoint yourself. If you leave it empty, Kepler finds the local exporter pod:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: kepler-gpu-config
  namespace: power-monitor
data:
  config.yaml: |
    experimental:
      gpu:
        enabled: true
        dcgmEndpoint: http://dcgm-exporter:9400/metrics
```

Kepler 0.12.0 itself also adds ARM64 build support, VirtualBox, VMware and Xen VM detection,
liveness and readiness probes, and a startup warning for config keys it doesn't recognize. See the
[Kepler v0.12.0 release notes](https://github.com/sustainable-computing-io/kepler/releases/tag/v0.12.0)
for the full list.

## Full user docs in the operator repository

The OpenShift install, configuration, troubleshooting, upgrade and migration guides from this site
now also live next to the code in [`docs/user`](https://github.com/sustainable-computing-io/kepler-operator/tree/v0.25.0/docs/user).
They were checked against the current APIs and security defaults on the way over.

## Under the hood

These changes don't show up in the generated release notes:

- **ARM64 build tooling.** The Dockerfile and Makefile can now cross-compile the operator and bundle
  for amd64 and arm64 with `docker buildx` ([#667](https://github.com/sustainable-computing-io/kepler-operator/pull/667)).
  The published 0.25.0 operator image is still amd64 only.
- **Tests moved to Ginkgo and Gomega**, following the Operator SDK recommendation ([#649](https://github.com/sustainable-computing-io/kepler-operator/pull/649))
- **Dependencies updated** for Go 1.24 ([#693](https://github.com/sustainable-computing-io/kepler-operator/pull/693)), and `govulncheck` pinned so CI keeps working ([#678](https://github.com/sustainable-computing-io/kepler-operator/pull/678))

## Upgrade note: `experimental.hwmon.enabled` is gone

With operator 0.24.0 (Kepler 0.11.4), `experimental.hwmon.enabled: true` made Kepler use HWMON instead of RAPL. The key was
renamed in Kepler 0.12.0 ([#676](https://github.com/sustainable-computing-io/kepler-operator/pull/676)),
and the operator now ignores the old name without a warning. If you set it, Kepler goes back to
RAPL after the upgrade.

To keep HWMON only, set `cpu.preferredMeters: [hwmon]`. If you also tune HWMON `zones` or
`chipRules`, use `experimental.hwmon.forceEnabled: true` instead for now, or Kepler 0.12.0 drops
that tuning. `forceEnabled` works but is deprecated.

## Try it out

**Kubernetes (Helm):**

```bash
helm upgrade --install kepler-operator \
  oci://quay.io/sustainable_computing_io/charts/kepler-operator \
  --version 0.25.0 \
  --namespace kepler-operator \
  --create-namespace
```

**OpenShift:** 0.25.0 is in the Community Operators catalog. With automatic approval, OLM upgrades
for you. Otherwise, approve the pending InstallPlan.

Back up your `PowerMonitor` first, and see the
[upgrade guide](https://github.com/sustainable-computing-io/kepler-operator/blob/v0.25.0/docs/user/guides/upgrading.md)
for details. Still on the legacy `Kepler` resource? Do the
[migration to PowerMonitor](https://github.com/sustainable-computing-io/kepler-operator/blob/v0.25.0/docs/user/guides/migration.md) first.

## Thanks

This release merged 22 pull requests, 11 of them from people and 11 from Dependabot. Thanks to
@vprashar2929, @vimalk78 and @kaiyiliu-strala for the changes, and to everyone who reviewed and
tested them.

## Get involved

- Chat with us in [#kepler-project](https://cloud-native.slack.com/archives/C05QK3KN3HT) on CNCF Slack
- Join the community call on the 1st and 3rd Tuesday of each month ([details](https://github.com/sustainable-computing-io/community/blob/main/community-event.md))
- Try it out and [open an issue](https://github.com/sustainable-computing-io/kepler-operator/issues) when something breaks
