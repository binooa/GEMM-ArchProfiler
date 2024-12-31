from m5.objects import *
import m5

# Set output directory
m5.core.setOutputDir("/home/binu/cnn_final/skylake/output")

# Create the system
root = Root(full_system=False)
root.system = System()

# Setup basic parameters
root.system.clk_domain = SrcClockDomain(clock="2.4GHz", voltage_domain=VoltageDomain())  # Skylake i3 typical clock
root.system.mem_mode = 'timing'
root.system.mem_ranges = [AddrRange('4GB')]

# Define memory bus
root.system.membus = SystemXBar()

# Setup multi-core CPU (2 cores for Skylake i3)
root.system.cpus = [TimingSimpleCPU(cpu_id=i) for i in range(2)]  # 2-core Skylake i3 setup

# Create interrupt controllers for each core
for cpu in root.system.cpus:
    cpu.createInterruptController()

# L1 Cache for each core
for cpu in root.system.cpus:
    cpu.icache = Cache(size="32kB", assoc=8)  # L1 instruction cache
    cpu.dcache = Cache(size="32kB", assoc=8)  # L1 data cache
    cpu.icache_port = cpu.icache.cpu_side
    cpu.dcache_port = cpu.dcache.cpu_side

# Shared L2 Cache
root.system.l2cache = Cache(size="256kB", assoc=4)  # L2 cache shared among cores
root.system.l2cache.cpu_side = [cpu.dcache.mem_side for cpu in root.system.cpus]
root.system.l2cache.mem_side = root.system.membus.cpu_side_ports

# Shared L3 Cache
root.system.l3cache = Cache(size="6MB", assoc=12)  # L3 cache shared among all cores
root.system.l3cache.cpu_side = root.system.l2cache.mem_side
root.system.l3cache.mem_side = root.system.membus.cpu_side_ports

# Memory controller
root.system.mem_ctrl = MemCtrl()
root.system.mem_ctrl.dram = DDR4_2400_8x8()  # Skylake i3 DDR4 support
root.system.mem_ctrl.dram.range = root.system.mem_ranges[0]
root.system.mem_ctrl.port = root.system.membus.mem_side_ports

# Power modeling
root.system.power_model = PowerModel()
root.system.power_model.voltage_domain = root.system.clk_domain.voltage_domain
root.system.power_model.cpu = root.system.cpus[0]  # Power modeled for the first CPU

# Tracers for each core
for cpu in root.system.cpus:
    cpu.tracer = TraceCPU()
    cpu.tracer.enable = True

# Set the SE workload
binary_path = "/home/binu/cnn_final/skylake/a.out"  # Adjust path
root.system.workload = SEWorkload.init_compatible(binary_path)

# Assign the workload to each CPU
for cpu in root.system.cpus:
    cpu.workload = Process(cmd=[binary_path])
    cpu.createThreads()

# Connect system port
root.system.system_port = root.system.membus.cpu_side_ports

# Run simulation
m5.instantiate()
print("Starting Skylake i3 Multi-Core simulation...")

exit_event = m5.simulate()

print(f"Exiting @ tick {m5.curTick()} because {exit_event.getCause()}")
