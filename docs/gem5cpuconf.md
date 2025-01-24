# **Detailed CPU and GEMM-ArchProfiler Configuration with gem5**

This file explains the setup and configuration of a system in gem5 for simulating the GEMM-ArchProfiler with O3CPU, multi-level caches, and checkpoints.

---

## **Table of Contents**
1. [Overview](#overview)
2. [Directory Setup](#directory-setup)
3. [System Configuration](#system-configuration)
4. [Checkpoint Handling](#checkpoint-handling)
5. [Simulation Execution](#simulation-execution)
6. [Results Analysis](#results-analysis)

---

## **Overview**

This guide covers a detailed gem5 setup to simulate:
- **O3 CPU configuration**
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
Ensure a directory for saving simulation checkpoints:
```bash
ls -l /opt/GEMM-ArchProfiler/output/checkpoints/darknet
```

---

## **System Configuration**

The following components are configured:
1. **Clock Domain and Memory Mode**:
   - Clock: `2GHz`
   - Memory Mode: `timing`
   - Memory Range: `4GiB`

2. **CPU Configuration**:
   - **Type**: `O3CPU`
   - **Caches**:
     - L1: 32KiB (ICache, DCache), 8-way associative, latency: 2
     - L2: 256KiB, 4-way associative, latency: 4
     - L3: 8MiB, 16-way associative, latency: 6

3. **Memory Controller**:
   - **Type**: `DDR3_1600_8x8`
   - Memory Range: `4GiB`

4. **Workload**:
   - **Binary Path**: `/opt/GEMM-ArchProfiler/darknet/darknet`
   - **Arguments**: `classifier predict cfg/imagenet1k.data cfg/darknet53.cfg darknet53.weights data/dog.jpg`

5. **Checkpoint Handling**:
   - **Resumption Option**: `resume_from_checkpoint`
   - **Fast-forward Tick**: `3700000000000` (optional)

---

## **Checkpoint Handling**

### **Directory Validation**
To avoid errors, ensure the checkpoint directory is managed appropriately:
- **Clear Directory**:
  If starting a new simulation:
  ```python
  def clear_checkpoint_dir(dir_path):
      if os.path.exists(dir_path):
          shutil.rmtree(dir_path)
          print(f"Cleared existing checkpoint directory: {dir_path}")
  ```

- **Check Directory Contents**:
  ```python
  def is_checkpoint_dir_empty(dir_path):
      return not os.listdir(dir_path)
  ```

---

## **Simulation Execution**

### **Fast-Forwarding Simulation**
If resuming from a checkpoint and requiring a fast-forward:
```python
if fast_forward_tick is not None:
    print(f"Fast-forwarding simulation to tick {fast_forward_tick}...")
    exit_event = m5.simulate(fast_forward_tick)
    print(f"Fast-forward completed at tick {m5.curTick()} with reason: {exit_event.getCause()}")
```

### **Running Detailed Simulation**
Simulation runs in a loop until completion or a checkpoint is created:
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

## **Results Analysis**

After the simulation, review the results in the `output` directory:

1. **Simulation Logs**:
   - Check logs for tick counts and checkpoint creation details.

2. **Output Files**:
   - Directory: `/opt/GEMM-ArchProfiler/output/darknet`
   - Key logs: `stats.txt`, checkpoint files, and trace logs.

---

---

[← Back to Main README](../README.md)