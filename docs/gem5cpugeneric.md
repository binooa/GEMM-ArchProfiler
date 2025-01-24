# **Detailed Customization of CPU and GEMM-ArchProfiler Configuration with gem5**

This file explains the setup and configuration of a system in gem5 for simulating the GEMM-ArchProfiler with O3CPU, multi-core setups, multi-level caches, and network-on-chip (NoC) components.

---

## **Table of Contents**
1. [Overview](#overview)
2. [Directory Setup](#directory-setup)
3. [System Configuration](#system-configuration)
4. [Memory Modes](#memory-modes)
5. [Checkpoint Handling](#checkpoint-handling)
6. [Simulation Execution](#simulation-execution)
7. [Advanced Configurations](#advanced-configurations)
8. [Results Analysis](#results-analysis)

---

## **Overview**

This guide covers a detailed gem5 setup to simulate:
- **O3 CPU configuration**
- Multi-core setup with NoC
- Multi-level cache hierarchy (L1, L2, L3)
- Memory setup with DDR3
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
- **Caches**:
  - L1: 32KiB (ICache, DCache) per core, 8-way associative, latency: 2
  - L2: Shared 256KiB cache, 4-way associative, latency: 4
  - L3: Shared 8MiB cache, 16-way associative, latency: 6

#### **CPU Setup Example**:
```python
# Define multi-core configuration
num_cores = 4
root.system.cpu = [O3CPU(cpu_id=i) for i in range(num_cores)]

# Setup caches for each core
for cpu in root.system.cpu:
    cpu.icache = Cache(size="32KiB", assoc=8, tag_latency=2, data_latency=2, response_latency=2)
    cpu.dcache = Cache(size="32KiB", assoc=8, tag_latency=2, data_latency=2, response_latency=2)
    cpu.icache_port = cpu.icache.cpu_side
    cpu.dcache_port = cpu.dcache.cpu_side

# Shared L2 and L3 caches
root.system.l2cache = Cache(size="256KiB", assoc=4, tag_latency=4, data_latency=4, response_latency=4)
root.system.l3cache = Cache(size="8MiB", assoc=16, tag_latency=6, data_latency=6, response_latency=6)
```

### **3. Network-on-Chip (NoC)**:
- **Interconnect**: Crossbar (SystemXBar) connects CPUs, caches, and memory controller.

#### **NoC Setup Example**:
```python
# Create crossbar interconnect
root.system.noc = SystemXBar()

# Connect L1 caches to NoC
for cpu in root.system.cpu:
    cpu.icache.mem_side = root.system.noc.cpu_side_ports
    cpu.dcache.mem_side = root.system.noc.cpu_side_ports

# Connect shared caches to NoC
root.system.l2cache.cpu_side = root.system.noc.mem_side_ports
root.system.l2cache.mem_side = root.system.l3cache.cpu_side_ports
root.system.l3cache.mem_side = root.system.membus.cpu_side_ports
```

### **4. Memory Controller**:
- **Type**: `DDR3_1600_8x8`
- Memory Range: `4GiB`

### **5. Workload**:
- **Binary Path**: `/opt/GEMM-ArchProfiler/darknet/darknet`
- **Arguments**: `classifier predict cfg/imagenet1k.data cfg/darknet53.cfg darknet53.weights data/dog.jpg`

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

[← Back to Main README](../README.md)

