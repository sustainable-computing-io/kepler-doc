# Kepler Power Model

In Kepler, with respective to available measurements, we provide a pod-level power with a mix of two
power modeling approaches:

## Modeling Approach

- **Power Ratio Modeling**: This modeling computes a finer-grained power by the usage ratio over the
  total summation of power. This modeling is used by default when the total power is known.

- **Power Estimation Modeling**: This modeling estimates a power by using usage metrics as input features
of the trained model. This modeling can be used even if the power metric cannot be measured. The estimation
can be done in three levels: Node total power (including fan, power supply, etc.), Node internal component
powers (such as CPU, Memory), Pod power.

  > **Note**: Also see [Get started with Kepler Model Server](../kepler_model_server/get_started.md)

- **Pre-trained Power Models**: We provide pre-trained power models for different deployment scenarios.
   Current x86_64 pre-trained model are developed in [Intel® Xeon® Processor E5-2667 v3][1]. Models with
   other architectures are coming soon. You can find these models in [Kepler Model DB][2]. These models
   support both power ratio modeling and power estimation modeling for both RAPL and ACPI power sources.
   The `AbsPower` models estimate both idle and dynamic power while the `DynPower` models only estimate
   dynamic power. The MAE (Mean Absolute Error) of these models are also published. Kepler container
   image has preloaded [acpi/AbsPower/BPFOnly/SGDRegressorTrainer_1.json][3] model for node energy estimate
   and [rapl/AbsPower/BPFOnly/SGDRegressorTrainer_1.json][4] for Container absolute power estimate.

## Usage Scenario

Scenario | Node Total Power | Node Component Powers | Pod Power
---|---|---|---
BM (x86 with power meter)| Measurement (e.g., ACPI)|  Measurement (RAPL)| Power Ratio
BM (x86 but no power meter)| Power Estimation | Measurement| Power Ratio
BM (non-x86 with power meter) | Measurement | Power Estimation | Power Ratio
BM (non-x86 and no power meter) | Power Estimation | Power Estimation | Power Ratio
VM with node info and power passthrough from BM (x86 with power meter)|Measurement + VM Mapping|Measurement + VM Mapping|Power Ratio
VM with node info and power passthrough from BM (x86 but no power meter)|Power Estimation|Measurement + VM Mapping|Power Ratio
VM with node info and power passthrough from BM (non-x86 with power meter)|Measurement + VM Mapping|Power Estimation|Power Ratio
VM with node info|Power Estimation|Power Estimation|Power Ratio
Pure VM|-|-|Power Estimation

[1]:https://github.com/sustainable-computing-io/kepler-model-db/tree/main/models
[2]:https://github.com/sustainable-computing-io/kepler-model-db/tree/main/models/v0.6/nx12
[3]:https://github.com/sustainable-computing-io/kepler-model-db/blob/main/models/v0.6/nx12/std_v0.6/acpi/AbsPower/BPFOnly/SGDRegressorTrainer_1.json
[4]:https://github.com/sustainable-computing-io/kepler-model-db/blob/main/models/v0.6/nx12/std_v0.6/rapl/AbsPower/BPFOnly/SGDRegressorTrainer_1.json
