from m5.objects import *
import m5

# Set output directory
m5.core.setOutputDir("/opt/GEMM-ArchProfiler/output")

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

# Shared L2 Cache
root.system.l2cache = Cache(size="2MB", assoc=8)  # Exynos shared L2 cache
root.system.l2cache.cpu_side = [cpu.dcache.mem_side for cpu in root.system.big_cpus + root.system.little_cpus]
root.system.l2cache.mem_side = root.system.membus.cpu_side_ports

# Memory controller
root.system.mem_ctrl = MemCtrl()
root.system.mem_ctrl.dram = DDR3_1600_8x8()  # Exynos supports DDR3
root.system.mem_ctrl.dram.range = root.system.mem_ranges[0]
root.system.mem_ctrl.port = root.system.membus.mem_side_ports

# Power modeling
root.system.power_model = PowerModel()
root.system.power_model.voltage_domain = root.system.clk_domain.voltage_domain
root.system.power_model.cpu = root.system.big_cpus[0]  # Power modeled for the first big core

# Tracers for each core
for cpu in root.system.big_cpus + root.system.little_cpus:
    cpu.tracer = TraceCPU()
    cpu.tracer.enable = True

# Set the SE workload

# Set up the workload for the system
binary_path = '/opt/GEMM-ArchProfiler/darknet/darknet'  # Path to the Darknet binary
args = ['classifier', 'predict', 'cfg/imagenet1k.data', 'cfg/darknet53.cfg', 'darknet53.weights', 'data/dog.jpg']


root.system.workload = SEWorkload.init_compatible(binary_path)

# Assign the workload to each CPU
for cpu in root.system.big_cpus + root.system.little_cpus:
    cpu.workload = Process(cmd=[binary_path] + args)
    cpu.createThreads()

# Connect system port
root.system.system_port = root.system.membus.cpu_side_ports

# Run simulation
m5.instantiate()
print("Starting Exynos Multi-Core simulation...")

exit_event = m5.simulate()

print(f"Exiting @ tick {m5.curTick()} because {exit_event.getCause()}")
