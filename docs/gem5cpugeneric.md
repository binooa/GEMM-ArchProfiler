# **Detailed CPU Customization Insructions for GEMM-ArchProfiler **

This file explains the setup and configuration of a system in gem5 for simulating the GEMM-ArchProfiler with O3CPU, multi-core setups, multi-level caches, and network-on-chip (NoC) components.

---

## **Table of Contents**
1. [Overview](#overview)
2. [Directory Setup](#directory-setup)
3. [CPU and Core Configuration](#cpu-and-core-configuration)
   - [Pipeline Width and Depth](#pipeline-width-and-depth)
   - [Integer and Floating-Point Units](#integer-and-floating-point-units)
   - [SIMD Units](#simd-units)
   - [Clock Speed and Voltage Domains](#clock-speed-and-voltage-domains)
4. [Cache Configuration](#cache-configuration)
5. [Memory System](#memory-system)
6. [Memory Modes](#memory-modes)
7. [Checkpoint Handling](#checkpoint-handling)
8. [Simulation Execution](#simulation-execution)
9. [Advanced Configurations](#advanced-configurations)
10. [Results Analysis](#results-analysis)
11. [Complete Python Configuration Code](#complete-python-configuration-code)

---

## **Overview**

This guide covers a detailed gem5 setup to simulate:
- **O3 CPU configuration**
- Multi-core setup with NoC
- Multi-level cache hierarchy (L1, L2, L3)
- Memory setup with DDR4
- Workload execution for GEMM-ArchProfiler using `darknet`
- Checkpoint creation and resumption

---

## **Directory Setup**

### **Output Directory**
Ensure the output directory exists before running the simulation:
```bash
ls -l /opt/GEMM-ArchProfiler/output/darknet
```

### **Checkpoint Directory**
Ensure a directory for saving simulation checkpoints:
```bash
ls -l /opt/GEMM-ArchProfiler/output/checkpoints/darknet
```

---

## **CPU and Core Configuration**

### **1. Multi-Core Setup**
- **Number of Cores**: 4 (can be adjusted as needed)
- **Type**: `O3CPU`
- **Core Connection**: Each core is connected to a crossbar interconnect (NoC).

```python
# Define multi-core configuration
num_cores = 4
root.system.cpu = [O3CPU(cpu_id=i) for i in range(num_cores)]
```

### **2. Pipeline Width and Depth**
```python
# Configure pipeline width and depth
root.system.cpu.fetchWidth = 4  # Example width
root.system.cpu.decodeWidth = 7  # Depth configuration
root.system.cpu.issueWidth = 32  # Maximum width
root.system.cpu.commitWidth = 4
```

### **3. Integer and Floating-Point Units**

#### **Integer ALU (IntAlu)**:
```python
root.system.cpu.numIntAlus = 4
root.system.cpu.intAluLatency = 1
```

#### **Integer Multipliers (IntMult)**:
```python
root.system.cpu.numIntMults = 1
root.system.cpu.intMultLatency = 4
```

#### **Floating-Point ALU (FPALU)**:
```python
root.system.cpu.numFpAlus = 1
root.system.cpu.fpAluLatency = 4
```

### **4. SIMD Units**
```python
# SIMD ALUs and Multipliers
root.system.cpu.numSimdAlus = 2
root.system.cpu.simdAluLatency = 5
```

### **5. Clock Speed and Voltage Domains**
```python
# Configure clock speed and voltage
root.system.cpu.clk_domain = SrcClockDomain(clock='3GHz', voltage_domain=VoltageDomain(voltage='1.2V'))
```

---

## **Cache Configuration**

### **L1 Instruction and Data Cache**
```python
root.system.cpu.icache = Cache(size="32KiB", assoc=8, tag_latency=1, data_latency=1, response_latency=1)
root.system.cpu.dcache = Cache(size="32KiB", assoc=8, tag_latency=1, data_latency=1, response_latency=4)
```

### **L2 Cache**
```python
root.system.l2cache = Cache(size="1MiB", assoc=16, tag_latency=12, data_latency=12, response_latency=6)
root.system.l2cache.prefetcher = StridePrefetcher()
root.system.l2cache.mshrs = 32
root.system.l2cache.write_buffers = 32
```

### **L3 Cache**
```python
root.system.l3cache = Cache(size="19.5MiB", assoc=11, tag_latency=44, data_latency=44, response_latency=21)
root.system.l3cache.prefetcher = StridePrefetcher()
root.system.l3cache.mshrs = 32
root.system.l3cache.write_buffers = 64
```

---

## **Memory System**

### **DRAM Configuration**
```python
root.system.mem_ctrl = MemCtrl()
root.system.mem_ctrl.dram = DDR4_2400_16x4(range=root.system.mem_ranges[0])
```

---

## **Memory Modes**

The `memory mode` defines how the memory system is modeled in gem5. Available options include:

### **1. `atomic` Mode**
- **Description**: Fast functional simulation with no detailed timing.
- **Use Case**: Early-stage testing.
- **Configuration**:
  ```python
  system.mem_mode = 'atomic'
  ```

### **2. `timing` Mode**
- **Description**: Detailed timing simulation for memory accesses.
- **Use Case**: Performance evaluation and bottleneck analysis.
- **Configuration**:
  ```python
  system.mem_mode = 'timing'
  ```

### **3. `atomic_noncaching` Mode**
- **Description**: Disables caching while using functional simulation.
- **Use Case**: Debugging raw memory behavior.
- **Configuration**:
  ```python
  system.mem_mode = 'atomic_noncaching'
  ```

### **4. `atomic_caching` Mode**
- **Description**: Functional simulation with basic cache support.
- **Use Case**: Lightweight cache modeling.
- **Configuration**:
  ```python
  system.mem_mode = 'atomic_caching'
  ```

### **5. `ideal` Mode**
- **Description**: Assumes no latency or bandwidth constraints for memory.
- **Use Case**: Baseline performance studies.
- **Configuration**:
  ```python
  system.mem_mode = 'ideal'
  ```

---

## **Checkpoint Handling**

### **Directory Validation**
To manage checkpoints effectively:

#### **Clear Directory**:
Clear existing checkpoints for a fresh simulation:
```python
def clear_checkpoint_dir(dir_path):
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
        print(f"Cleared existing checkpoint directory: {dir_path}")
```

#### **Check Directory Contents**:
Validate checkpoint directory contents:
```python
def is_checkpoint_dir_empty(dir_path):
    return not os.listdir(dir_path)
```

---

## **Simulation Execution**

### **Initialization**
If resuming from a checkpoint:
```python
if resume_from_checkpoint and not is_checkpoint_dir_empty(checkpoint_dir):
    print(f"Resuming simulation from checkpoint: {checkpoint_dir}")
    m5.instantiate(checkpoint_dir)
else:
    clear_checkpoint_dir(checkpoint_dir)
    print("Starting fresh simulation...")
    m5.instantiate()
```

### **Fast-Forwarding Simulation**
Optional fast-forward to a specific tick:
```python
if fast_forward_tick is not None:
    print(f"Fast-forwarding simulation to tick {fast_forward_tick}...")
    exit_event = m5.simulate(fast_forward_tick)
    print(f"Fast-forward completed at tick {m5.curTick()} with reason: {exit_event.getCause()}")
```

### **Running Detailed Simulation**
Simulation runs in a loop until completion or checkpoint creation:
```python
while True:
    exit_event = m5.simulate()
    print(f"Exited at tick {m5.curTick()} with reason: {exit_event.getCause()}")

    if not checkpoint_created and m5.curTick() >= checkpoint_tick:
        print(f"Creating checkpoint at tick {m5.curTick()}...")
        m5.checkpoint(checkpoint_dir)
        checkpoint_created = True

    if exit_event.getCause() == "checkpoint":
        continue
    else:
        break
```

---

## **Advanced Configurations**

### **Out-of-Order (O3) CPU Pipeline Tuning**:
Fine-tune O3CPU parameters:
```python
system.cpu.fetchWidth = 4
system.cpu.decodeWidth = 4
system.cpu.issueWidth = 4
system.cpu.commitWidth = 4
```

---

## **Results Analysis**

After the simulation, review results in the `output` directory:

1. **Simulation Logs**:
   - Check logs for tick counts and checkpoint creation details.

2. **Output Files**:
   - Directory: `/opt/GEMM-ArchProfiler/output/darknet`
   - Key logs: `stats.txt`, checkpoint files, and trace logs.

---

## **Complete Python Configuration Code**

Below is a Python configuration code for reference, combining all the discussed features:


```python

import os
import shutil
from m5.objects import *
import m5

# Set output and checkpoint directories
m5.core.setOutputDir("/opt/GEMM-ArchProfiler/output/darknet")
checkpoint_dir = "/opt/GEMM-ArchProfiler/output/checkpoints/darknet"

# Options
resume_from_checkpoint = False
fast_forward_tick = None
checkpoint_tick = 3700000000000
intermediate_dump_interval = 100000000000  # Interval for intermediate dumps

# Clear checkpoint directory
if not resume_from_checkpoint:
    if os.path.exists(checkpoint_dir):
        shutil.rmtree(checkpoint_dir)

# Create system
root = Root(full_system=False)
root.system = System()
root.system.clk_domain = SrcClockDomain(clock="3GHz", voltage_domain=VoltageDomain(voltage="1.2V"))
root.system.mem_mode = 'timing'
root.system.mem_ranges = [AddrRange('4GiB')]

# CPU configuration
num_cores = 4
root.system.cpu = [O3CPU(cpu_id=i) for i in range(num_cores)]
for cpu in root.system.cpu:
    cpu.fetchWidth = 4
    cpu.decodeWidth = 7
    cpu.issueWidth = 32
    cpu.commitWidth = 4
    cpu.numIntAlus = 4
    cpu.intAluLatency = 1
    cpu.numIntMults = 1
    cpu.intMultLatency = 4
    cpu.numFpAlus = 1
    cpu.fpAluLatency = 4
    cpu.numSimdAlus = 2
    cpu.simdAluLatency = 5
    cpu.clk_domain = SrcClockDomain(clock="3GHz", voltage_domain=VoltageDomain(voltage="1.2V"))

# L1 Cache configuration
for cpu in root.system.cpu:
    cpu.icache = Cache(size="32KiB", assoc=8, tag_latency=1, data_latency=1, response_latency=1)
    cpu.dcache = Cache(size="32KiB", assoc=8, tag_latency=1, data_latency=1, response_latency=4)

# L2 Cache configuration
root.system.l2cache = Cache(size="1MiB", assoc=16, tag_latency=12, data_latency=12, response_latency=6)
root.system.l2cache.prefetcher = StridePrefetcher()
root.system.l2cache.mshrs = 32
root.system.l2cache.write_buffers = 32

# L3 Cache configuration
root.system.l3cache = Cache(size="19.5MiB", assoc=11, tag_latency=44, data_latency=44, response_latency=21)
root.system.l3cache.prefetcher = StridePrefetcher()
root.system.l3cache.mshrs = 32
root.system.l3cache.write_buffers = 64

# Connect caches
for cpu in root.system.cpu:
    cpu.icache_port = cpu.icache.cpu_side
    cpu.dcache_port = cpu.dcache.cpu_side

root.system.l2cache.cpu_side = root.system.cpu[0].icache.mem_side
root.system.l2cache.mem_side = root.system.l3cache.cpu_side
root.system.l3cache.mem_side = root.system.membus.cpu_side_ports

# Memory Controller
root.system.mem_ctrl = MemCtrl()
root.system.mem_ctrl.dram = DDR4_2400_16x4(range=root.system.mem_ranges[0])
root.system.mem_ctrl.port = root.system.membus.mem_side_ports

# System Port
root.system.system_port = root.system.membus.cpu_side_ports

# Set up the workload for the system
binary_path = '/opt/GEMM-ArchProfiler/darknet/darknet'
args = ['classifier', 'predict', 'cfg/imagenet1k.data', 'cfg/darknet53.cfg', 'darknet53.weights', 'data/dog.jpg']

# Debugging output
print(f"Binary Path: {binary_path}")
print(f"Arguments: {args}")

# Initialize SEWorkload
root.system.workload = SEWorkload.init_compatible(binary_path)

# Assign the workload to the CPU
process = Process(pid=100, cmd=[binary_path] + args)
root.system.cpu[0].workload = process
root.system.cpu[0].createThreads()

# Instantiate and run simulation
if resume_from_checkpoint and os.path.exists(checkpoint_dir):
    print(f"Resuming from checkpoint: {checkpoint_dir}")
    m5.instantiate(checkpoint_dir)
else:
    print("Starting new simulation...")
    m5.instantiate()

if fast_forward_tick:
    print(f"Fast-forwarding simulation to tick {fast_forward_tick}...")
    exit_event = m5.simulate(fast_forward_tick)
    print(f"Fast-forward completed at tick {m5.curTick()} due to: {exit_event.getCause()}")

print("Starting detailed simulation...")
next_dump_tick = intermediate_dump_interval
while True:
    exit_event = m5.simulate()
    print(f"Exited at tick {m5.curTick()} due to: {exit_event.getCause()}")
    if m5.curTick() >= next_dump_tick:
        print(f"Creating intermediate dump at tick {m5.curTick()}...")
        m5.dumpStats()
        next_dump_tick += intermediate_dump_interval
    if m5.curTick() >= checkpoint_tick and not resume_from_checkpoint:
        print(f"Creating checkpoint at tick {m5.curTick()}...")
        m5.checkpoint(checkpoint_dir)
        break
    if exit_event.getCause() == "simulate() limit reached":
        break
print("Simulation complete.")

```


---

[← Back to Main README](../README.md)