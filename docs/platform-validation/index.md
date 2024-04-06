# Platform Validation Framework

In this document, we will share the design and implementation of Kepler's platform validation framework.
Please refer to enhancement [document](https://github.com/sustainable-computing-io/kepler/blob/main/enhancements/platform-validation.md)
for the feature initiative and scope.

Kepler should and will integrate with various of hardware platforms, the framework will first use Intel X86
BareMetal platform as example to show the platform validation mechanism and workflows. Other platform owners
could use this document as reference to add their specific test cases and workflows to make Kepler better
engage with their platforms.

## Mechanism and methodology

Platform validation work should be done automatically, could follow the standard Github Action workflow
mechanism and let the target platform be self-hosted runner. See Github action official document for more
details about [self-hosted runner](https://docs.github.com/en/actions/hosting-your-own-runners).

Platform validation cases should follow the current Kepler's Ginkgo test framework.

We could leverage the Ginkgo [Reporting Infrastructure](https://onsi.github.io/ginkgo/#reporting-infrastructure)
to generate test report in both human and machine readable formats, such as JSON.

Platform validation cases should support both validity and accuracy check on Kepler/Prometheus exposed data.

Take Intel X86 BareMetal platform's validation as example, we have introduced an independent RAPL-based energy
collection and power consumption calculation tool called `validator`.

The current work mechanism and features of `validator` are simple:

1. It could detect the current platform's CPU model type.
2. It could detect the current platform's in-band RAPL components support status and OOB platform power source
  support status.
3. It uses specific sampling count(configurable, by default 20 sampling cycles) with specific sampling interval
  (configurable, by default 15 seconds) to collect the specific components' RAPL values and calculate the power
  consumption of each sampling, then achieve the mean value of node components power among those sampling cycles.

Test cases could use above sampling and calculation results as comparison base to check the Kepler exported and
Prometheus aggregated query results.

For other platforms, developers may use other specific measurement methods and tools to implement similar
validation targets and logic.

### Data validity check

Intel X86 Platforms could have different CPU models which are exported by Kepler, this should be verified in
independent way. The case setup and execution should have no extra dependencies on the platform OS and software
packages/libraries.

For Intel X86 CPUs, especially the new coming ones, the cpu model detail information comes with `cpuid` tool.
On Linux Distros such as Ubuntu, the `cpuid` tool version is often not up-to-date, so it is better way to design
an OS agnostic container to perform the test.

For Intel X86 platforms, the specific RAPL domains available vary across product segments.

Platforms targeting the client segment support the following RAPL domain hierarchy:

* Package

* Two power planes: PP0 and PP1 (PP1 may reflect to uncore devices)

Platforms targeting the server segment support the following RAPL domain hierarchy:

* Package

* Power plane: PP0

* DRAM

We need to check the current hardware's component power source support status and check if the exposed data is
expected (zero or non-zero).

### Data accuracy check

For Intel X86 platforms, since the RAPL based system power collection is available on BareMetal, Kepler uses
[Power Ratio Modeling](https://sustainable-computing.io/design/power_model/).

Such power attribution mechanism accuracy should be checked.

We need to introduce an independent and platform agnostic way to collect the node components power info.

Due to the root privilege limit on the access of the RAPL SYSFS files, we need to use privileged container
to perform the test.

For node level power accuracy check, the comparison logic is simple and straightforward, while for pod/container
level power accuracy check, the logic is a little bit complicated and need some assumptions.

1. RAPL energy is node/package level, so we could only use RAPL sampling delta to calculate the power change
introduced by application deployment and undeployment.

2. On the other hand, application power consumption data could be queried from Prometheus where Kepler's exported
time-series metrics are aggregated.

3. On a clean/idle platform, without other tenants' workloads interference, we could have a simple assumption that
the power increase introduced by the specific application deployment is equal to the test container calculated power
delta in (1).

4. On a busy platform, with other tenants' workloads running in parallel, in container or in VM, for instance, the
scenarios become complicated. Since the interference power may be fluctuated and unable to detect, the Kepler
`Power Ratio Modeling` check criteria is unknown, now we just dump all the available data and leave the result for
evaluation after platform validation test.

5. On some CPU/GPU-intensive workloads deployment platform, such as AI/AIGC inference pipeline's worker node, the
`validator` raw data could be used to measure the approximate power consumption contribution of those inferencing
pods/containers. We can then compare the Kepler demonstrated power consumption data, either in PromQL query
result(automation) or on Grafana Dashboard(manual test).

This is also meaningful test case for the carbon footprint accuracy check on AI/AIGC workloads.

## Validation workflow

See example Github action workflow [here](https://github.com/sustainable-computing-io/kepler/blob/main/.github/workflows/platform-validation.yml).

The workflow is similar as the e2e integration test workflow, has two phases jobs:

### Artifacts build

Build both the `Kepler` container image and the `Validator` container image.

The current Validator image refers to the Kepler image build mechanism to build from a GPU image to support GPU
case. We may simply build it from UBI image later.

Since it is an independent energy collector other than Kepler, those eBPF stuffs will not be bumped into the
container.

### Platform validation test

The major steps in this job are as follows:

1. Download artifacts and import images.

2. Run `validator` image to collect energy and calculate node components power consumption data before deploying
  local-dev-cluster(Kind in this example)

3. Use Kepler action to deploy local-dev-cluster(Kind) with local registry support and full kube-prometheus
  monitoring stack.

4. Run `validator` image again to collect energy and calculate node components power consumption data before
  deploying Kepler exporter.

5. Deploy Kepler exporter in local-dev-cluster above and let it be monitored by Prometheus.

6. Run `validator` image the 3rd time to collect energy and calculate node components power consumption data
  after deploying Kepler exporter.

7. Run platform-validation test scripts, do below things:

    1. `port forwarding` kepler-exporter and prometheus-k8s service to let their ports accessible to Ginkgo
    test code.

    2. Use `ginkgo` CLI to run [test suite](https://github.com/sustainable-computing-io/kepler/blob/main/e2e/platform-validation),
    execute cases described in section [Mechanism and methodology](https://github.com/sustainable-computing-io/kepler-doc/blob/main/docs/platform-validation/index.md#mechanism-and-methodology)
    above and generate test report in `platform_validation_report.json` file assigned by `--json-report` parameter.

    3. Dump necessary test log and data for post-test evaluation use.

8. Cleanup the test environment(undeploy Kepler exporter, the local-dev-cluster and the local registry).

> **Note**: In specific test cases, the power data delta of step 4 and 2 could be comparison base for
local-dev-cluster's power consumption; while the power data delta of step 6 and 4 could be the kepler
exporter's power comparison base.

## Validation result evaluation

Check validation report for any failure cases.

Check accuracy cases comparison result. Node level cases should be more accurate than pod/container
level cases, make analysis on any abnormal results and figure out RCAs for them.

Manual/automation check for specific workloads on specific platforms, see example in (5) of
`Data accuracy check` section above.

**TODO**: There is an analyzer under developing for abnormality detection in platform validation test,
it will be integrated into the current workflow when it is ready.

## Further works

Identify issues based on the validation report on specific platforms and figure out solutions.

Extend platform scenario from BareMetal to VM.

Design validation cases for VM scenario and support more accurate power attribution among VM-based
workloads and container/process-based workloads.
