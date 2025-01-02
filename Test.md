# GEMM-ArchProfiler

**Integrated Testbed for GEMM Performance Benchmarking in real CNN Workload on gem5 architectural simulator**

---

## Overview
GEMM-ArchProfiler provides a unified framework for benchmarking General Matrix Multiplication (GEMM) algorithms in Convolutional Neural Network (CNN) performance on the gem5 architectural simulator. It is designed to help researchers and engineers analyze, profile, and optimize GEMM performance across diverse CPU architectures.

The idea is to profile GEMM algorithms, which form the core of any CNN-based implementation. As we progress toward edge-based systems, GEMM must be verified under realistic workloads. While GEMM, as an independent algorithm implementation, may work on any target architecture, real CNN implementations with real workloads may not yield appropriate results. Moreover, the environment plays a critical role, particularly for studies on memory, cache memory, and energy usage across different architectures.

GEMM-ArchProfiler serves as a testbed for CPU-based simulation work, supporting both single-threaded and multi-threaded environments. It includes pre-built GEMM implementations, and users can also test new GEMM implementations on real CNN workloads with customizable CPU configurations, either existing or preferred.

---

## Prerequisites
Ensure your system meets the following requirements:
- **Operating System**: Ubuntu 22.04 or later
- **Required Packages**: 
  - Build tools
  - Python3
  - Development libraries

---

## Frameworks and Packages Used
GEMM-ArchProfiler leverages three major frameworks/packages:

1. **gem5 Architectural Simulator**: A detailed architectural simulation platform for CPU performance analysis. https://www.gem5.org/documentation/general_docs/building
2. **C-based CNN Implementation**: Supports major CNN architectures such as Darknet, DenseNet, and ResNet. https://github.com/pjreddie/darknet
3. **Customized CNN Implementation**: Includes scripts and source code for:
   - GEMM Implementations   
   - GEMM Testing
   - gem5 Profiling
   - Analysis of gem5 log files

---

## Setup Instructions

### Step 1: Create a Directory for GEMM-ArchProfiler
```bash
sudo mkdir -p /opt/GEMM-ArchProfiler
```

### Step 2: Change Ownership of the Directory
```bash
sudo chown $USER:$USER /opt/GEMM-ArchProfiler
```

### Step 3: Change to the Directory
```bash
cd /opt/GEMM-ArchProfiler
```

### Step 4: gem5 Installation Setup

#### Install Required Dependencies
Run the following command to install all the necessary dependencies for building and running gem5:
```bash
sudo apt install build-essential scons python3-dev git pre-commit zlib1g zlib1g-dev \
    libprotobuf-dev protobuf-compiler libprotoc-dev libgoogle-perftools-dev \
    libboost-all-dev libhdf5-serial-dev python3-pydot python3-venv python3-tk mypy \
    m4 libcapstone-dev libpng-dev libelf-dev pkg-config wget cmake doxygen dos2unix
```

#### Clone the gem5 Repository
## About gem5

gem5 is a modular and highly flexible open-source architectural simulator widely used in computer architecture research and education. It provides a comprehensive framework for simulating a variety of systems, including CPUs, GPUs, and memory subsystems, across multiple ISAs (Instruction Set Architectures) like X86, ARM, RISC-V, and more.

gem5 supports detailed modeling of processor microarchitectures, cache hierarchies, and interconnects, allowing researchers to evaluate system-level performance, energy efficiency, and design trade-offs. Its versatility enables the simulation of full-system workloads as well as bare-metal applications.

With its support for profiling tools like `gprof`, gem5 is an indispensable tool for performance analysis and optimization in the design of next-generation computing systems.

```bash
git clone https://github.com/gem5/gem5
```

#### Build gem5 with Profiling Support
Compile gem5 with the `--gprof` flag to enable compatibility with the `gprof` profiling tool:
```bash
cd gem5
scons build/X86/gem5.debug ARCH=X86 --gprof
```
> **Note**: The `--gprof` flag enables detailed performance profiling of GEMM operations during simulation. 

> **Note:** : The compilation process may take approximately one hour to complete, depending on your system's specifications. Ensure your system has sufficient computational resources and allocate adequate time for this build process.

---

### Step 5: Change Directory Back to GEMM-ArchProfiler
```bash
cd /opt/GEMM-ArchProfiler
```

### Step 6: Clone and Set Up Darknet
## About Darknet

Darknet is an open-source neural network framework written in C and CUDA, designed for speed and flexibility. It is widely used for object detection tasks and supports implementations like YOLO (You Only Look Once). Darknet offers modularity, making it easy to configure and extend for custom use cases, while maintaining high performance for both training and inference on various hardware platforms, including CPUs and GPUs.

Darknet comes with a configuration script that allows the implementation of a wide range of popular CNN architectures. For the testbed, the authors utilized architectures such as Darknet53, DenseNet201, and ResNet152 to demonstrate its versatility and performance.

```bash
git clone https://github.com/pjreddie/darknet
cd darknet
```

### Step 7: Replace Existing Makefile in Darknet Directory
> **Alert**: Make sure your current working directory is set to `/opt/GEMM-ArchProfiler/darknet` before proceeding.
```bash
rm Makefile
wget https://github.com/binooa/GEMM-ArchProfiler/raw/main/Makefile -O Makefile
```

### Step 8: Replace Existing gemm.c File in Darknet Source Directory
> **Alert**: Make sure your current working directory is set to `/opt/GEMM-ArchProfiler/darknet` before proceeding.
```bash
rm src/gemm.c
wget https://github.com/binooa/GEMM-ArchProfiler/raw/main/src/gemm.c -O src/gemm.c
```
### Step 9: Copy dummy_gpu.c File in Darknet Source Directory
> **Alert**: Make sure your current working directory is set to `/opt/GEMM-ArchProfiler/darknet` before proceeding.
```bash
wget https://github.com/binooa/GEMM-ArchProfiler/raw/main/src/dummy_gpu.c -O src/dummy_gpu.c
```

### Step 10: Make and create executable
> **Alert**: Make sure your current working directory is set to `/opt/GEMM-ArchProfiler/darknet` before proceeding.

```bash
make
```


### Step 11: Download CNN Pretrained Weights
> **Alert**: Make sure your current working directory is set to `/opt/GEMM-ArchProfiler/darknet` before proceeding.
```bash
cd /opt/GEMM-ArchProfiler/darknet
wget https://pjreddie.com/media/files/darknet53.weights
wget https://pjreddie.com/media/files/densenet201.weights
wget https://pjreddie.com/media/files/resnet152.weights
```



### Step 12: Change Directory Back to GEMM-ArchProfiler
```bash
cd /opt/GEMM-ArchProfiler
```

### Step 13: Download CPU Configuration Files
```bash
git init
git remote add origin https://github.com/binooa/GEMM-ArchProfiler.git
git config core.sparseCheckout true
echo "cpuconf/" >> .git/info/sparse-checkout
git pull origin main
```

### Step 14: Execution Bug Fixing
> **Alert**: If any, errors identified during execution, try.

```bash
cat -A /opt/GEMM-ArchProfiler/darknet/cfg/imagenet1k.data
dos2unix /opt/GEMM-ArchProfiler/darknet/cfg/imagenet1k.data

cat -A /opt/GEMM-ArchProfiler/darknet/data/imagenet.shortnames.list
dos2unix /opt/GEMM-ArchProfiler/darknet/data/imagenet.shortnames.list

cat -A /opt/GEMM-ArchProfiler/darknet/cfg/darknet53.cfg
dos2unix /opt/GEMM-ArchProfiler/darknet/cfg/darknet53.cfg

cat -A /opt/GEMM-ArchProfiler/darknet/cfg/densenet201.cfg
dos2unix /opt/GEMM-ArchProfiler/darknet/cfg/densenet201.cfg

cat -A /opt/GEMM-ArchProfiler/darknet/cfg/resnet152.cfg
dos2unix /opt/GEMM-ArchProfiler/darknet/cfg/resnet152.cfg
```

### Step 15: Run the Simulation
> **Alert**: Make sure your current working directory is set to `/opt/GEMM-ArchProfiler` before proceeding.
```bash
cd /opt/GEMM-ArchProfiler
wget https://github.com/binooa/GEMM-ArchProfiler/raw/main/simulate.sh -O /opt/GEMM-ArchProfiler/simulate.sh
chmod a+x /opt/GEMM-ArchProfiler/simulate.sh
/opt/GEMM-ArchProfiler/simulate.sh
```


## Usage
Once gem5 is successfully installed:
1. Use the provided configuration files and workloads to simulate and profile GEMM operations.
2. Run performance benchmarks for GEMM and CNNs on the gem5 simulator.

---

## License
This project is licensed under the [MIT License](LICENSE).

---

## Contributions
Contributions are welcome! Please submit issues and pull requests to improve GEMM-ArchProfiler.

---

## Contact
For any queries or support, please contact:
- **Email**: [your-email@example.com](mailto:your-email@example.com)
- **GitHub**: [Your GitHub Profile](https://github.com/your-profile)