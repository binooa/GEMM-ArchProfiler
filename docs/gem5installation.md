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

### Clone the gem5 Repository
### About gem5

gem5 is a modular and highly flexible open-source architectural simulator widely used in computer architecture research and education. It provides a comprehensive framework for simulating a variety of systems, including CPUs, GPUs, and memory subsystems, across multiple ISAs (Instruction Set Architectures) like X86, ARM, RISC-V, and more.

gem5 supports detailed modeling of processor microarchitectures, cache hierarchies, and interconnects, allowing researchers to evaluate system-level performance, energy efficiency, and design trade-offs. Its versatility enables the simulation of full-system workloads as well as bare-metal applications.

With its support for profiling tools like `gprof`, gem5 is an indispensable tool for performance analysis and optimization in the design of next-generation computing systems.

```bash
git clone https://github.com/gem5/gem5
```

### Build gem5 
```bash
cd gem5
scons build/X86/gem5.opt  ARCH=X86 -j$(nproc)
```

(Optional) Enable Profiling
To enable profiling with tools like gprof, recompile gem5 with the --gprof flag:
```bash
scons build/X86/gem5.debug ARCH=X86 --gprof
```
> **Note**: The `--gprof` flag enables detailed performance profiling of GEMM operations during simulation. 

> **Note:** : The compilation process may take approximately one hour to complete, depending on your system's specifications. Ensure your system has sufficient computational resources and allocate adequate time for this build process.

### Build the m5 Utility 
Navigate to the m5 utility directory and build the required libraries for the X86 architecture
```bash
cd /opt/GEMM-ArchProfiler/gem5/util/m5
scons build/x86/out/libm5.a
```
If the library file libm5.a or libm5.so is missing, this command will generate it in the build/x86/out directory.


#### Check gem5 

### Step 5: Verify the Build
Check if the gem5 binary was successfully built by listing the build/X86/ directory:

```bash
cd /opt/GEMM-ArchProfiler/gem5/
ls build/X86/
```
You should see a file named gem5.opt or gem5.debug.

### Step 6: Run a Basic Test
To ensure that gem5 is working, run a simple test simulation:

```bash
build/X86/gem5.opt configs/example/se.py --cmd=/bin/ls
```
This runs a simple simulation using the X86 architecture and the ls command.

### Step 7: Verify the m5 Utility
Check if the libm5.a or libm5.so file exists:
```bash
ls /opt/GEMM-ArchProfiler/gem5/util/m5/build/x86/out
```


---

[← Back to Main README](../README.md)