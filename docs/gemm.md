## GEMM Algorithm(s) Implementation in Customised darknet CNN library - Setup Instructions

---

**Note**: Ensure that you have successfully completed the gem5 installation and  darknet CNN library & Customization of darknet CNN library as outlined in the previous sections before proceeding further.

# GEMM Implementation with gem5 Integration

This project provides an efficient and modular implementation of **General Matrix Multiplication (GEMM)** operations, supporting various optimization strategies and integration with the **gem5 simulator** for performance profiling.

---

## Features

### 1. Flexible GEMM Modes
- **Default GEMM**: A simple, straightforward implementation for matrix multiplication tasks.
- **Tiled GEMM**: Uses matrix blocking to optimize cache utilization and parallel processing, with a configurable block size.
- **Optimized GEMM**: Implements loop unrolling to reduce loop overhead and improve computational efficiency.

### 2. Integration with gem5
- Supports performance profiling with `m5_reset_stats`, `m5_dump_stats`, and `m5_exit` commands.
- Enables simulation checkpointing via `m5_checkpoint`.

### 3. Parallel Processing
- Uses OpenMP to support multi-threaded execution for all GEMM modes.

### 4. Debugging and Logging
- Logs matrix dimensions, scaling factors, and operation counts for debugging and performance monitoring.

### 5. Extensibility
- Easily add new GEMM algorithms by modifying specific functions and updating the `Makefile`.

---

### Step 15: Replace Existing gemm.c File in Darknet Source Directory
> **Alert**: Make sure your current working directory is set to `/opt/GEMM-ArchProfiler/darknet` before proceeding.
```bash
cd /opt/GEMM-ArchProfiler/darknet/
rm src/gemm.c
wget https://github.com/binooa/GEMM-ArchProfiler/raw/main/src/gemm.c -O src/gemm.c
```

### Step 16: ReMake and create executable
> **Alert**: Make sure your current working directory is set to `/opt/GEMM-ArchProfiler/darknet` before proceeding.

```bash
cd /opt/GEMM-ArchProfiler/darknet
make clean
make
```

---

[← Back to Main README](../README.md)