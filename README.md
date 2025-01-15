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
3. **Customization of CNN Implementation**: Includes scripts and source code for:
   - GEMM Implementations   
   - GEMM Testing
   - gem5 Profiling
   - Analysis of gem5 log files

---

- [Introduction](docs/introduction.md)  

**Note**: Installation of the packages must be done in the exact order specified in the documentation. Skipping or reordering steps may result in errors.
- [Step 1 : Installation of gem5 architectural simulator](docs/gem5installation.md)
- [Step 2 : Installation of darknet CNN library & Customization of darknet CNN library ](docs/darknetinstallation.md)
- [Step 3 : GEMM Algorithm(s) Implementation in Customised darknet CNN library](docs/gemm.md)
- [Step 4 : GEM5 Simulator CPU Configuration(s)](docs/gem5simulation.md)
- [Step 5 : Compile & Simulate](docs/runsimulation.md)
- [Step 6 : GEM5 Simulation Log Processor](docs/darkentinstallation.md)
- [Step 6 : Analyse Simulation Results](docs/development.md)
- [Contributing](docs/contributing.md)
