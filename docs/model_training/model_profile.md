# Model Profile

To form a group of machines (nodes), the idea is to run a benchmark suite towards a bunch of machines, collect performance reported by the benchmarks, and apply clustering algorithm such as *kmeans*.

For each group (`node_type`), we make a profile composing of background power when the resource usage is almost constant without user workload, minimum, maximum power for each power components (e.g., core, uncore, dram, package, platform), and normalization scaler (i.e., MinMaxScaler), standardization scaler (i.e., StandardScaler) for each [feature group](./pipeline.md#model-features).

Check the profiling tool [here](https://raw.githubusercontent.com/sustainable-computing-io/kepler-model-server/main/src/profile).
