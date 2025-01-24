# **Detailed Instructions on Customizing CPU for adding more features for GEMM-ArchProfiler**

This file explains the setup and configuration of a system in gem5 for simulating the GEMM-ArchProfiler with O3CPU, multi-core setups, multi-level caches, and network-on-chip (NoC) components.

---

## **Table of Contents**
1. [Overview](#overview)
2. [Directory Setup](#directory-setup)
3. [System Configuration](#system-configuration)
4. [Execution Units](#execution-units)
5. [Cache Configuration](#cache-configuration)
6. [Memory Modes](#memory-modes)
7. [Checkpoint Handling](#checkpoint-handling)
8. [Simulation Execution](#simulation-execution)
9. [Advanced Configurations](#advanced-configurations)
10. [Results Analysis](#results-analysis)

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
Ensure directory for saving simulation checkpoints:
```bash
ls -l /opt/GEMM-ArchProfiler/output/checkpoints/darknet
```

---

## **System Configuration**

The following components are configured:

### **1. Clock Domain and Memory Mode**:
- Clock: `2GHz`
- Memory Mode: `timing`
- Memory Range: `4GiB`

### **2. Multi-Core CPU Configuration**:
- **Number of Cores**: 4 (can be adjusted as needed)
- **Type**: `O3CPU`
- **Core Connection**: Each core is connected to a crossbar interconnect (NoC).

---

## **Execution Units**

### **Pipeline Width and Depth**:
```python
root.system.cpu.fetchWidth = 4  # Example width
root.system.cpu.decodeWidth = 7  # Depth configuration
root.system.cpu.issueWidth = 32  # Maximum width
root.system.cpu.commitWidth = 4
```

### **Integer ALU (IntAlu)**:
```python
root.system.cpu.numIntAlus = 4
root.system.cpu.intAluLatency = 1
```

### **Integer Multipliers (IntMult)**:
```python
root.system.cpu.numIntMults = 1
root.system.cpu.intMultLatency = 4
```

### **Floating-Point ALU (FPALU)**:
```python
root.system.cpu.numFpAlus = 1
root.system.cpu.fpAluLatency = 4
```

### **SIMD Units**:
```python
root.system.cpu.numSimdAlus = 2
root.system.cpu.simdAluLatency = 5
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

### **Clock Speed and Voltage Domains**:
Modify clock speed and voltage:
```python
system.clk_domain = SrcClockDomain(clock='3GHz', voltage_domain=VoltageDomain(voltage='1.2V'))
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

## **License**

This setup and configuration are distributed under the MIT License. Contributions and feedback are welcome!