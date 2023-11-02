# Kepler Energy Sources

## Background

### RAPL - Running Average Power Limit

Intel’s Running Average Power Limit (RAPL) is a hardware feature which allows to monitor energy consumption across different domains of the CPU chip, attached DRAM and on-chip GPU. This feature was introduced in Intel’s Sandy Bridge architecture and has evolved in the later versions of Intel’s processing architecture. With RAPL it is possible to programmatically get real time data on the power consumption of the CPU package and its components, as well as of the DRAM memory that the CPU is managing.

RAPL provides two different functionalities. 
Allows energy consumption to be measured at very fine granularity and a high sampling rate. 
Allows limiting (or capping) the average power consumption of different components inside the processor, which also limits the thermal output of the processor

Kepler makes use of the energy consumption measurement capability.

RAPL supports multiple power domains. The RAPL power domain is a physically meaningful domain (e.g., Processor Package, DRAM etc) for power management. Each power domain informs the energy consumption of the domain. 

RAPL provides the following power domains for both measuring and limiting energy consumption:

 - **Package**: Package (PKG) domain measures the energy consumption of the entire socket. It includes the consumption of all the cores, integrated graphics and also the uncore components (last level caches, memory controller).
 - **Power Plane 0** (PP0) : measures the energy consumption of all processor cores on the socket.
 - **Power Plane 1** (PP1) : measures the energy consumption of processor graphics (GPU) on the socket (desktop models only).
 - **DRAM**: measures the energy consumption of random access memory (RAM) attached to the integrated memory controller.



The support for different power domains varies according to the processor model.



## Reading Energy values

### Using RAPL MSR (Model Specific Registers)

The RAPL energy counters can be accessed through model-specific registers (MSRs). The counters are 32-bit registers that indicate the energy consumed since the processor was booted up. The counters are updated approximately once every millisecond. The energy is counted in multiples of model-specific energy units. Sandy Bridge uses energy units of 15.3 microjoules, whereas Haswell and Skylake uses units of 61 microjoules. The units can be read from specific MSRs before doing energy calculations.

The MSRs can be accessed directly on Linux using the msr driver in the kernel. Reading RAPL domain values directly from MSRs requires detecting the CPU model and reading the RAPL energy units before reading the RAPL domain. Once the CPU model is detected, the RAPL domains can be read per package of the CPU by reading the corresponding ’MSR status’ register. 

There are basically two types of events that RAPL events report
Static Events: thermal specifications, maximum and minimum power caps, and time windows.
Dynamic Events: RAPL domain energy readings from the chip such as PKG, PP0, PP1 or DRAM 

### Using RAPL Sysfs 
From Linux Kernel version 3.13 onwards, RAPL values can be read using “Power Capping Framework” [2].  

Linux Power Capping framework exposes power capping devices to user space via sysfs in the form of a tree of objects. 

This sysfs tree is mounted at `/sys/class/powercap/intel-rapl`. When RAPL is available, this path exists and kepler reads energy values from this path.

### Using kernel driver xgene-hwmon
Using Xgene-hwmon driver kepler reads power from APM X-Gene SoC. It supports reading CPU and IO power in micro watts. 

### Using eBpf perf events 
Not used in kepler

### Using PAPI library
Performance Application Programming Interface (PAPI) 
Not used in kepler


Kepler chooses to use one enenry sources in the following order of preference:
1. Sysfs
2. MSR
3. Hwmon


## Permissions required
### MSRs
Root access is required to use the msr driver

### Sysfs (powercap)
Root access is required to use powercap driver




## References
 [1] [RAPL in Action: Experiences in Using RAPL for Power Measurements](https://helda.helsinki.fi/server/api/core/bitstreams/bdc6c9a5-74d4-494b-ae83-860625a665ce/content)

 [2] [RA Power Capping Framework](https://www.kernel.org/doc/html/next/power/powercap/powercap.html)

 [3] [RA Kernel driver xgene-hwmon](https://docs.kernel.org/hwmon/xgene-hwmon.html)

 [4] [RA Performance Application Programming Interface (PAPI)](https://icl.utk.edu/papi/)
