# GEMM-ArchProfiler
  **Integrated Testbed for GEMM Performance Benchmarking in real CNN Workload on gem5 architectural simulator**


# GEMMBench

**Integrated Testbed for GEMM and CNN Performance Benchmarking on gem5**

---

## Overview
GEMMBench provides a unified framework for benchmarking General Matrix Multiplication (GEMM) algorithms in Convolutional Neural Network (CNN) performance on the gem5 architectural simulator. It is designed to help researchers and engineers analyze, profile, and optimize GEMM performance across diverse CPU architectures.

The idea is to profile GEMM algorithms, which form the core of any CNN-based implementation. As we progress toward edge-based systems, GEMM must be verified under realistic workloads. While GEMM, as an independent algorithm implementation, may work on any target architecture, real CNN implementations with real workloads may not yield appropriate results. Moreover, the environment plays a critical role, particularly for studies on memory, cache memory, and energy usage across different architectures.

GEMMBench serves as a testbed for CPU-based simulation work, supporting both single-threaded and multi-threaded environments. It includes pre-built GEMM implementations, and users can also test new GEMM implementations on real CNN workloads with customizable CPU configurations, either existing or preferred.

---

## Prerequisites
Ensure your system meets the following requirements:
- **Operating System**: Ubuntu 24.04 or later
- **gem5 Version**: v24.0 or higher
- **Required Packages**: 
  - Build tools
  - Python3
  - Development libraries

---

## Setup Instructions

### Step 1: Create a Directory for GEMMBench
```bash
sudo mkdir -p /opt/GEMMBench
```

### Step 2: Change Ownership of the Directory
```bash
sudo chown $USER:$USER /opt/GEMMBench
```

### Step 3: Change to the Directory
```bash
cd /opt/GEMMBench
```

### Step 4: gem5 Installation Setup

#### Install Required Dependencies
Run the following command to install all the necessary dependencies for building and running gem5:
```bash
sudo apt install build-essential scons python3-dev git pre-commit zlib1g zlib1g-dev \
    libprotobuf-dev protobuf-compiler libprotoc-dev libgoogle-perftools-dev \
    libboost-all-dev libhdf5-serial-dev python3-pydot python3-venv python3-tk mypy \
    m4 libcapstone-dev libpng-dev libelf-dev pkg-config wget cmake doxygen
```

#### Clone the gem5 Repository
```bash
git clone https://github.com/gem5/gem5
```

#### Build gem5 with Profiling Support
Compile gem5 with the `--gprof` flag to enable compatibility with the `gprof` profiling tool:
```bash
scons build/ARM/gem5.debug --gprof
```
> **Note**: The `--gprof` flag enables detailed performance profiling of GEMM operations during simulation.

---

## Usage
Once gem5 is successfully installed:
1. Use the provided configuration files and workloads to simulate and profile GEMM operations.
2. Run performance benchmarks for GEMM and CNNs on the gem5 simulator.

---

## License
This project is licensed under the [MIT License](LICENSE).

---

## Contributions
Contributions are welcome! Please submit issues and pull requests to improve GEMMBench.

---

## Contact
For any queries or support, please contact:
- **Email**: [your-email@example.com](mailto:your-email@example.com)
- **GitHub**: [Your GitHub Profile](https://github.com/your-profile)
