from m5.objects import *
import m5
import os
import sys

# Set output directory
output_dir = "/opt/GEMM-ArchProfiler/output"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
m5.core.setOutputDir(output_dir)

# Create the system
root = Root(full_system=False)
root.system = System()

# Setup basic parameters
root.system.clk_domain = SrcClockDomain(clock="2GHz", voltage_domain=VoltageDomain())  # Exynos Cortex-A15 clock
root.system.mem_mode = 'timing'
root.system.mem_ranges = [AddrRange('2GB')]

# Define memory bus
root.system.membus = SystemXBar()

# Setup big.LITTLE CPU configuration
# Big cores (2 Cortex-A15 cores)
root.system.big_cpus = [TimingSimpleCPU(cpu_id=i) for i in range(2)]

# Little cores (2 Cortex-A7 cores)
root.system.little_cpus = [TimingSimpleCPU(cpu_id=i+2) for i in range(2)]

# Create interrupt controllers for all cores
for cpu in root.system.big_cpus + root.system.little_cpus:
    cpu.createInterruptController()

# L1 Cache for each core
for cpu in root.system.big_cpus:
    cpu.icache = Cache(size="32kB", assoc=2)  # Cortex-A15 L1 instruction cache
    cpu.dcache = Cache(size="32kB", assoc=2)  # Cortex-A15 L1 data cache
    cpu.icache_port = cpu.icache.cpu_side
    cpu.dcache_port = cpu.dcache.cpu_side

for cpu in root.system.little_cpus:
    cpu.icache = Cache(size="32kB", assoc=2)  # Cortex-A7 L1 instruction cache
    cpu.dcache = Cache(size="32kB", assoc=2)  # Cortex-A7 L1 data cache
    cpu.icache_port = cpu.icache.cpu_side
    cpu.dcache_port = cpu.dcache.cpu_side

# Create a crossbar for CPU-side connections
root.system.cpu_xbar = SystemXBar()

# Connect L1 dcache ports to the crossbar
for cpu in root.system.big_cpus + root.system.little_cpus:
    cpu.dcache.mem_side = root.system.cpu_xbar.slave

# Shared L2 Cache
root.system.l2cache = Cache(size="2MB", assoc=8)  # Exynos shared L2 cache
root.system.l2cache.cpu_side = root.system.cpu_xbar.master
root.system.l2cache.mem_side = root.system.membus.slave

# Memory controller
root.system.mem_ctrl = MemCtrl()
root.system.mem_ctrl.dram = DDR3_1600_8x8()  # Exynos supports DDR3
root.system.mem_ctrl.dram.range = root.system.mem_ranges[0]
root.system.mem_ctrl.port = root.system.membus.mem_side_ports

# Power modeling for all cores
for cpu in root.system.big_cpus + root.system.little_cpus:
    cpu.power_model = PowerModel()
    cpu.power_model.voltage_domain = root.system.clk_domain.voltage_domain

# Enable tracers conditionally
enable_tracing = True  # Set to False to disable tracers
for cpu in root.system.big_cpus + root.system.little_cpus:
    if enable_tracing:
        cpu.tracer = TraceCPU()
        cpu.tracer.enable = True

# Set SE workload
binary_path = '/opt/GEMM-ArchProfiler/darknet/darknet'  # Default binary path
args = ['classifier', 'predict', 'cfg/imagenet1k.data', 'cfg/darknet53.cfg', 'darknet53.weights', 'data/dog.jpg']

# Accept command-line arguments for flexibility
if len(sys.argv) > 1:
    binary_path = sys.argv[1]
    args = sys.argv[2:]

# Set up the workload process
process = Process(cmd=[binary_path] + args)

# Assign the same workload process to each CPU
for cpu in root.system.big_cpus + root.system.little_cpus:
    cpu.workload = process
    cpu.createThreads()

# Connect system port
root.system.system_port = root.system.membus.cpu_side_ports

# Run simulation
m5.instantiate()
print("Starting Exynos Multi-Core simulation...")

exit_event = m5.simulate()

print(f"Exiting @ tick {m5.curTick()} because {exit_event.getCause()}")
