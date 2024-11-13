# Hardware Engagement

In this document, we will share our steps as how to engage Kepler with a specific hardware device.
Considering there are many different hardware devices, we will just write down major steps here as current stage.
You are able to take this out as a todo list and step by step to make Kepler engage with your own hardware device.

## Stage 0 Proof

In this Stage, we will focus on basic data can be collected by golang, and you can build your own Kepler which running on your device well.
The following steps can running in parallel.

### Binary build and container build

Currently Kepler container image is from a GPU image to support GPU case. Considering a general case for IOT device.
You may need to build Kepler from UBI image. We recommend you following steps below to setup a local build env and try to build.

1. Find a linux OS.
1. Install Kepler dependencies as eBPF golang(BCC), linux header and build Kepler (from main branch or latest release branch) binary.
1. (Optional)Modify [dockerfile](https://github.com/sustainable-computing-io/kepler/tree/main/build) to build the container image.

### Power consumption API

Currently, we use power consumption API as RAPL or ACPI.
For some of the devices, you may need to find your own way to get power consumption, and implement in golang for Kepler usage.
For further plan, please ref [here](https://github.com/sustainable-computing-io/kepler/issues/644)

### eBPF data

Currently, we rely on eBPF to obtain key cpu, irq  and perf information about a process.
Hence,  refer to the documentation of [cilium/ebpf](https://github.com/cilium/ebpf) to test whether these Go packages work well on your device.

Please let us know if you need any further adjustments!

## Stage 1 Integration with ratio

During this Stage, we are going to ref Kepler model. To integrate and implement your own logic specific to your device and deep dive into Power consumption API.

### Scope

You should know the scope of the Power consumption API. How many API do you have? Is it categorized by CPU/memory/IO or not?

### Interval

You should know the intervals of the Power consumption API.
As Kepler collects eBPF data in each 3s by default, you should know the interval and make them in same time slot.

### Verify

You can cross check and verify the data.

## Stage 2 Model_training

TBD
