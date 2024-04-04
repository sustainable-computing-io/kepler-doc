# Node Profile

We form a group of machines (nodes) called [node type](./pipeline.md#node-spec) based on processor model, the number of cores, the number of chips, memory size, and maximum CPU frequency. When collecting the data from the bare metal machine, these attributes are automatically extracted and kept as a machine spec in json format.

A power model will be built per node type. For each group of node type, we make a profile composing of background power when the resource usage is almost constant without user workload, minimum, maximum power for each power components (e.g., core, uncore, dram, package, platform), and normalization scaler (i.e., MinMaxScaler), standardization scaler (i.e., StandardScaler) for each [feature group](./pipeline.md#available-metrics).

Node specification is composed of:

- processor *- CPU processor model name*
- cores *- Number of CPU cores*
- chips *- Number of chips*
- memory_gb *- Memory size in GB*
- cpu_freq_mhz *- Maximum CPU frequency in MHz*
