Kepler Power Model
===================
In Kepler, with respective to available measurements, we provide a pod-level power with a mix of two power modeling approaches:

- **Power Ratio Modeling**: This modeling computes a finer-grained power by the usage ratio over the total summation of power. This modeling is used by default when the total power is known.

- **Power Estimation Modeling**: This modeling estimates a power by using usage metrics as input features of the trained model. This modeling can be used even if the power metric cannot be measured. The estimation can be done in three levels: Node total power (including fan, power supply, etc.), Node internal component powers (such as CPU, Memory), Pod power.

See .. figure:: ../power_estimate/index.rst

.. list-table:: Power Model
   :widths: 25 25 25 25
   :header-rows: 1

   * - Scenario
     - Node Total Power
     - Node Component Powers
     - Pod Power
   * - BM (x86 with power meter)
     - Measurement (e.g., ACPI)
     - Measurement (RAPL)
     - Power Ratio
   * - BM (x86 but no power meter)
     - Power Estimation
     - Measurement
     - Power Ratio
   * - BM (non-x86 with power meter)
     - Measurement
     - Power Estimation
     - Power Ratio
   * - BM (non-x86 and no power meter)
     - Power Estimation
     - Power Estimation
     - Power Ratio
   * - VM with node info and power passthrough from BM (x86 with power meter)
     - Measurement + VM Mapping
     - Measurement + VM Mapping
     - Power Ratio
   * - VM with node info and power passthrough from BM (x86 but no power meter)
     - Power Estimation
     - Measurement + VM Mapping
     - Power Ratio
   * - VM with node info and power passthrough from BM (non-x86 with power meter)
     - Measurement + VM Mapping
     - Power Estimation
     - Power Ratio
   * - VM with node info
     - Power Estimation
     - Power Estimation
     - Power Ratio
   * - Pure VM
     - \-
     - \-
     - Power Estimation