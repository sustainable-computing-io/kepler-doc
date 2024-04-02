# eBPF in Kepler

## Contents

- [Background](#background)
  - [What is eBPF ?](#what-is-ebpf)
  - [What is a kprobe?](#what-is-a-kprobe)
    - [How to list all currently registered kprobes ?](#list-kprobes)
  - [Hardware CPU Events Monitoring](#hardware-cpu-events-monitoring)
    - [How to check if kernel supports perf_event_open?](#check-support-perf_event_open)
- [Kernel routine probed by kepler](#kernel-routine-probed-by-kepler)
- [Hardware CPU events monitored by Kepler](#hardware-cpu-events-monitored-by-kepler)
- [Calculate process (aka task) total CPU time](#calculate-total-cpu-time)
- [Calculate task CPU cycles](#calculate-total-cpu-cycle)
- [Calculate task Ref CPU cycles](#calculate-total-cpu-ref-cycle)
- [Calculate task CPU instructions](#calculate-total-cpu-instr)
- [Calculate task Cache misses](#calculate-total-cpu-cache-miss)
- [Calculate 'On CPU Average Frequency'](#calculate-on-cpu-avg-freq)
- [Process Table](#process-table)
- [References](#references)

## Background

<!-- markdownlint-disable MD033 -->
### What is eBPF ? <a name="what-is-ebpf"></a>

eBPF is a revolutionary technology with origins in the Linux kernel that can run sandboxed programs in a privileged context such as the operating system kernel. It is used to safely and efficiently extend the capabilities of the kernel without requiring to change kernel source code or load kernel modules. [1]

### What is a kprobe?

KProbes is a debugging mechanism for the Linux kernel which can also be used for monitoring events inside a production system. KProbes enables you to dynamically break into any kernel routine and collect debugging and performance information non-disruptively. You can trap at almost any kernel code address, specifying a handler routine to be invoked when the breakpoint is hit.  [2]

#### How to list all currently registered kprobes ? <a name="list-kprobes"></a>

```bash
sudo cat /sys/kernel/debug/kprobes/list
```

### Hardware CPU Events Monitoring

Performance counters are special hardware registers available on most modern CPUs. These registers count the number of certain types of hw events: such as instructions executed, cache misses suffered, or branches mis-predicted -without slowing down the kernel or applications. [4]

Using syscall `perf_event_open` [5], Linux allows to set up performance monitoring for hardware and software performance. It returns a file descriptor to read performance information.
This syscall takes `pid` and `cpuid` as parameters. Kepler uses `pid == -1` and `cpuid` as actual cpu id.
This combination of pid and cpu allows measuring all process/threads on the specified cpu.

#### How to check if kernel supports `perf_event_open`? <a name="check-support-perf_event_open"></a>

Check presence of `/proc/sys/kernel/perf_event_paranoid` to know if kernel supports `perf_event_open` and what is allowed to be measured

```bash
   The perf_event_paranoid file can be set to restrict
   access to the performance counters.

   2      allow only user-space measurements (default since Linux 4.6).
   1      allow both kernel and user measurements (default before Linux 4.6).
   0      allow access to CPU-specific data but not raw tracepoint samples.
  -1      no restrictions.


   Measuring all process/threads required CAP_SYS_ADMIN capability or a value less than 1 in above file
```

**CAP_SYS_ADMIN** is highest level of capability, it must have some security implications

## Kernel routine probed by kepler

Kepler traps into `finish_task_switch` kernel function [3], which is responsible for cleaning up after a task switch occurs. Since the probe is `kprobe` it is called before `finish_task_switch` is called (instead of a `kretprobe` which is called after the probed function returns).

When a context switch occurs inside the kernel, the function `finish_task_switch` is called on the new task which is going to use the CPU. This function receives an argument of type `task_struct*` which contains all the information about the task which is leaving the CPU.[3]

The probe function in kepler is

```c
int kprobe__finish_task_switch(struct pt_regs *ctx, struct task_struct *prev)
```

The first argument is of type pointer to a `pt_regs` struct which refers to the structure that holds the register state of the CPU at the time of the kernel function entry. This struct contains fields that correspond to the CPU registers, such as general-purpose registers (e.g., r0, r1, etc.), stack pointer (sp), program counter (pc), and other architectural-specific registers.
The second argument is a pointer to a `task_struct` which contains the task information for the previous task, i.e. the task which is leaving the CPU.

## Hardware CPU events monitored by Kepler

Kepler opens monitoring for following hardware cpu events

| PERF Type          | Perf Count Type              | Description                                                                                                                                                                               | Array name <br>(in bpf program) |
|--------------------|------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------|
| PERF_TYPE_HARDWARE | PERF_COUNT_HW_CPU_CYCLES     | Total CPU cycles; can get affected by CPU frequency scaling                                                                                                                               | cpu_cycles_hc_reader            |
| PERF_TYPE_HARDWARE | PERF_COUNT_HW_REF_CPU_CYCLES | Total CPU cycles; not affected by CPU frequency scaling                                                                                                                                   | cpu_ref_cycles_hc_reader        |
| PERF_TYPE_HARDWARE | PERF_COUNT_HW_INSTRUCTIONS   | Retired instructions.  Be careful, these can be affected by various issues, most notably hardware interrupt counts.                                                                       | cpu_instr_hc_reader             |
| PERF_TYPE_HARDWARE | PERF_COUNT_HW_CACHE_MISSES   | Cache misses. Usually this indicates Last Level Cache misses; this is intended to be used in conjunction with the PERF_COUNT_HW_CACHE_REFERENCES event to calculate cache miss rates. | cache_miss_hc_reader            |

Performance counters are accessed via special file descriptors. There's one file descriptor per virtual counter used. The file descriptor is associated with the corresponding array. When bcc wrapper functions are used, it reads the corresponding fd, and return values.

## Calculate process (aka task) total CPU time <a name="calculate-total-cpu-time"></a>

The ebpf program (`bpfassets/bcc/bcc.c`) maintains a mapping from a `<pid, cpuid>` pair to a timestamp. The timestamp signifies the moment `kprobe__finish_task_switch` was called for pid when this pid was to be scheduled on cpu `<cpuid>`

```c
// <Task PID, CPUID> => Context Switch Start time

typedef struct pid_time_t { u32 pid; u32 cpu; } pid_time_t;
BPF_HASH(pid_time, pid_time_t);
// pid_time is the name of variable which if of type map
```

Within the function `get_on_cpu_time`, the difference between the current timestamp and timestamp from the `pid_time` map is used to calculate the `on_cpu_time_delta` for previous task on the current cpu.

This `on_cpu_time_delta` is used to accumulate the `process_run_time` metrics for the previous task.

## Calculate task CPU cycles <a name="calculate-total-cpu-cycle"></a>

For task cpu cycles, the bpf program maintains an array named `cpu_cycles`, indexed by `cpuid`. This contains values from perf array `cpu_cycles_hc_reader`, which is a perf event type array.

On each task switch:

- current value is read from perf counter array cpu_cycles_hc_reader
- the previous value from cpu_cycles is retrieved
- delta is calculated by subtracting prev value from current value
- the current value is copied back to cpu_cycles for next task switch

The delta thus calculated is the cpu cycles used by the process leaving the cpu

## Calculate task Ref CPU cycles <a name="calculate-total-cpu-ref-cycle"></a>

Same process as calculating CPU cycles, difference being perf array used is `cpu_ref_cycles_hc_reader` and prev value is stored in `cpu_ref_cycles`

## Calculate task CPU instructions <a name="calculate-total-cpu-instr"></a>

Same process as calculating CPU cycles, difference being perf array used is `cpu_instr_hc_reader` and prev value is stored in `cpu_instr`

## Calculate task Cache misses <a name="calculate-total-cpu-cache-miss"></a>

Same process as calculating CPU cycles, difference being perf array used is `cache_miss_hc_reader` and prev value is stored in `cache_miss`

## Calculate 'On CPU Average Frequency' <a name="calculate-on-cpu-avg-freq"></a>
<!-- markdownlint-enable MD033 -->

```c
avg_freq = ((on_cpu_cycles_delta * CPU_REF_FREQ) / on_cpu_ref_cycles_delta) * HZ;

CPU_REF_FREQ = 2500
HZ = 1000
```

This value is stored in array `cpu_freq_array`

## Calculate 'page cache hit'

The probe function in kepler `kprobe__set_page_dirty` and `kprobe__mark_page_accessed` are used to track page cache hit for write and read action respectively.

## Process Table

The bpf program maintains a bpf hash named `processes`. This hash maintains data calculated for a process. Kepler reads values from this hash ( known as a `Table` in bcc ) and generates metrics.

| Key | Value            |Description                                                                                               |
|-----|------------------|-----------------------------------------------------------------------------------------------|
| pid | cgroupid         | Process CGroupID                                                                              |
|     | pid              | Process ID                                                                                    |
|     | process_run_time | Total time a process occupies CPU (calculated each time process leaves CPU on context switch) |
|     | cpu_cycles       | Total CPU cycles consumed by process                                                          |
|     | cpu_instr        | Total CPU instructions consumed by process                                                    |
|     | cache_miss       | Total Cache miss by process                                                                   |
|     | page_cache_hit   | Total hit of the page cache                                                                   |
|     | vec_nr           | Total number of soft irq handles by process (max 10)                                          |
|     | comm             | Process name (max length 16)                                                                  |

This hash is read by the kernel collector in `container_hc_collector.go` for metrics collection.

## References

 [1] [https://ebpf.io/what-is-ebpf/](https://ebpf.io/what-is-ebpf/) , [https://www.splunk.com/en_us/blog/learn/what-is-ebpf.html](https://www.splunk.com/en_us/blog/learn/what-is-ebpf.html) , [https://www.tigera.io/learn/guides/ebpf/](https://www.tigera.io/learn/guides/ebpf/)

 [2] [An introduction to KProbes](https://lwn.net/Articles/132196/) , [Kernel Probes (Kprobes)](https://docs.kernel.org/trace/kprobes.html)

 [3] [finish_task_switch - clean up after a task-switch](https://elixir.bootlin.com/linux/v6.4-rc7/source/kernel/sched/core.c#L5157)

 [4] [Performance Counters for Linux](https://elixir.bootlin.com/linux/latest/source/tools/perf/design.txt)

 [5] [perf_event_open(2) — Linux manual page](https://www.man7.org/linux/man-pages/man2/perf_event_open.2.html)
