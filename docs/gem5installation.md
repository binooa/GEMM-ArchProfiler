## GEM5 Setup Instructions

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