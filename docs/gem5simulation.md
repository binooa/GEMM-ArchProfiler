## GEM5 Simulator - CPU Configuration(s) - Setup Instructions

---

**Note**: Ensure that you have successfully completed the all previous sections successfully.


### Step 17: Download CPU Configuration Files
```bash
git init
git remote add origin https://github.com/binooa/GEMM-ArchProfiler.git
git config core.sparseCheckout true
echo "cpuconf/" >> .git/info/sparse-checkout
git pull origin main
```
[← GEM5 CPU Configuration Details used for Simulation](gem5cpuconf.md)

[← GEM5 CPU Customization Instructions to change CPU Configuration](gem5cpugeneric.md)

---

## Sample Configuration Files for Intel and ARM Architectures


| Architecture | gem5 CPU Configuration | Remarks |
|----------|----------|----------|
| IntelCorei3_6100U   | [IntelCorei3_6100U Configuration](https://github.com/binooa/GEMM-ArchProfiler/blob/main/cpuconf/IntelCorei3_6100U.py)   | The Intel Core i3-6100U is a 6th Generation Skylake processor designed for low-power mobile computing and embedded applications. It features 2 cores and 4 threads with a base clock speed of 2.30 GHz. The processor has a three-level cache hierarchy, consisting of 32 KB L1 cache per core, 256 KB L2 cache per core, and a shared 3 MB L3 cache. It supports up to 8 GB DDR3 RAM at 1600 MHz and includes AVX2, SSE4.1, and SSE4.2 instruction set extensions. With a TDP (Thermal Design Power) of 15W, the i3-6100U is optimized for energy-efficient performance in laptops and embedded systems.|
| Samsung Exynos5422   | [Samusung Exynos5422 Configuration](https://github.com/binooa/GEMM-ArchProfiler/blob/main/cpuconf/exynos5422.py)   | The Samsung Exynos 5422 is an octa-core mobile processor based on ARM big.LITTLE architecture, featuring four Cortex-A15 cores clocked at 2.0 GHz for high-performance tasks and four Cortex-A7 cores clocked at 1.4 GHz for power efficiency. It includes a Mali-T628 MP6 GPU, supporting OpenGL ES 3.1, OpenCL 1.2, and DirectX 11, making it suitable for graphics-intensive applications. The processor has a three-level cache hierarchy, consisting of 32 KB L1 cache per core, 512 KB L2 cache per core cluster, and a shared 2 MB L3 cache. It supports up to 2 GB LPDDR3 RAM at 1600 MHz and features NEON, ARMv7-A, and TrustZone security extensions. With its HMP (Heterogeneous Multi-Processing) support, the Exynos 5422 dynamically schedules workloads across its CPU clusters for optimized power consumption and performance.  |
| AUP PYNQ-Z2   | [AUP PYNQ-Z2 Configuration](https://github.com/binooa/GEMM-ArchProfiler/blob/main/cpuconf/pynqz2.py)   | The ARM Cortex-A9 is a 32-bit processor core based on the ARMv7-A architecture, widely used in embedded platforms such as the PYNQ-Z2 development board. It features a dual-issue, partially out-of-order pipeline that enhances instruction throughput, and supports both the ARM and Thumb/Thumb-2 instruction sets for efficient and flexible execution. On the PYNQ-Z2, each Cortex-A9 core includes a 32 KB L1 instruction cache and a 32 KB L1 data cache, along with a shared 512 KB L2 cache, enabling fast access to frequently used data and instructions. The processor supports virtual memory through an integrated Memory Management Unit (MMU), and typically includes an optional Vector Floating Point (VFP) unit for accelerating floating-point operations. Additional features include branch prediction, virtual register renaming, out-of-order write-back, and cache line fill support. Designed to deliver over 50% higher performance compared to its predecessor, the Cortex-A8, the Cortex-A9 on the PYNQ-Z2 provides a strong balance of computational capability and power efficiency, making it ideal for real-time processing, embedded control, and hardware-software co-design experiments.  |
| Intel Core i7-11370H   | [Intel Core i7-11370H Configuration](https://github.com/binooa/GEMM-ArchProfiler/blob/main/cpuconf/IntelCorei7_11370H.py)   | The Intel Core i7-11370H is a 64-bit quad-core processor based on the 11th Generation Intel Tigerlake microarchitecture, designed for high-performance mobile and embedded computing platforms. Operating at a base frequency of 3.30 GHz, it features an out-of-order execution pipeline and supports modern instruction set extensions such as AVX2, SSE4.1, and SSE4.2, enabling efficient execution of data-parallel workloads and multimedia applications. Each core is equipped with a 32 KB L1 instruction cache, a 48 KB L1 data cache, and a private 1.25 MB L2 cache, while a shared 12 MB L3 cache facilitates rapid data access across all cores. The processor supports simultaneous multithreading (SMT), commonly known as Hyper-Threading, allowing each core to manage two execution threads. However, gem5 currently does not support Hyper-Threading, and simulations are limited to modeling one thread per core. Despite this limitation, gem5 can approximate the core-level behavior of the i7-11370H using the O3CPU model, allowing detailed analysis of pipeline utilization, memory hierarchy interactions, and performance tuning. This makes it suitable for conducting design-space exploration and architectural studies for high-performance x86 systems. |




### GEM5 Simulation - Binary Execution Configuration for Intel and ARM Architectures
This configuration executes a **binary file** within the GEM5 simulation environment. The setup runs the **Darknet-based classifier** to evaluate **GEMM workloads** in CNN-based AI models. It can be replaced with Resnet OR Denset.

---

#### **Binary Execution Details** 

| Parameter | Value |
|-----------|----------------------------------------------------------|
| **Binary Path** | `/opt/GEMM-ArchProfiler/darknet/darknet` |
| **Execution Mode** | `classifier` |
| **Operation** | `predict` |
| **Dataset Configuration** | `cfg/imagenet1k.data` |
| **Model Configuration** | `cfg/darknet53.cfg` |
| **Pre-trained Weights** | `darknet53.weights` |
| **Input Image** | `data/dog.jpg` |

---

## Note

Simulation may take five hours or more, depending on the specifications of the system running the simulation. Ensure sufficient system resources and plan accordingly. 

Before performing the simulation, the **`simulate.sh`** file must be modified to ensure that the updated configuration file is used for simulation.

```
4)
    echo "You selected Darkent on IntelCorei3_6100U."
    cd /opt/GEMM-ArchProfiler/darknet
    export GEMM_LOG_DIR="/opt/GEMM-ArchProfiler/output/resnet"               
    nohup /opt/GEMM-ArchProfiler/gem5/build/X86/gem5.opt --outdir=/opt/GEMM-ArchProfiler/gem5_output /opt/GEMM-ArchProfiler/cpuconf/IntelCorei3_6100U.py > /opt/GEMM-ArchProfiler/output/darknet_inteli1/darknet_inteli1_status.log 2>&1 &
    ;;

5)
    echo "You selected Darkent on Samsung Exynos5422."
    cd /opt/GEMM-ArchProfiler/darknet
    export GEMM_LOG_DIR="/opt/GEMM-ArchProfiler/output/resnet"               
    nohup /opt/GEMM-ArchProfiler/gem5/build/X86/gem5.opt --outdir=/opt/GEMM-ArchProfiler/gem5_output /opt/GEMM-ArchProfiler/cpuconf/exynos5422.py > /opt/GEMM-ArchProfiler/output/darknet_exyons5422/darknet_exyons5422_status.log 2>&1 &
    ;;
```
---
[← Back to Main README](../README.md)