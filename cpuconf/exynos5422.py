import os
import shutil
from m5.objects import *
import m5

# Set output directory
m5.core.setOutputDir("/opt/GEMM-ArchProfiler/output/exynos5422")

# Checkpoint directory
checkpoint_dir = "/opt/GEMM-ArchProfiler/output/checkpoints/exynos5422"

# Options
resume_from_checkpoint = False
fast_forward_tick = None  

# Function to check if the checkpoint directory is empty
def is_checkpoint_dir_empty(dir_path):
    return not os.listdir(dir_path)

# Function to clear the checkpoint directory
def clear_checkpoint_dir(dir_path):
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
        print(f"Cleared existing checkpoint directory: {dir_path}")

# Create the system
root = Root(full_system=False)
root.system = System()

# Setup basic parameters
root.system.clk_domain = SrcClockDomain(clock="2GHz", voltage_domain=VoltageDomain())  # Max Clock Speed
root.system.mem_mode = 'timing'  
root.system.mem_ranges = [AddrRange('2GiB')]  # 2GB LPDDR3 RAM

# Define memory bus
root.system.membus = SystemXBar()

# Configure big.LITTLE CPU setup
root.system.big_cores = [O3CPU(cpu_id=i) for i in range(4)]  # Cortex-A15 (High Performance)
root.system.little_cores = [MinorCPU(cpu_id=i + 4) for i in range(4)]  # Cortex-A7 (Power Efficient)

# Create interrupt controllers for each CPU
for cpu in root.system.big_cores + root.system.little_cores:
    cpu.createInterruptController()
    cpu.interrupts[0].pio = root.system.membus.mem_side_ports
    cpu.interrupts[0].int_requestor = root.system.membus.cpu_side_ports

# L1 Caches
for cpu in root.system.big_cores:
    cpu.icache = Cache(size="32KiB", assoc=8, tag_latency=2, data_latency=2, response_latency=2)
    cpu.dcache = Cache(size="32KiB", assoc=8, tag_latency=2, data_latency=2, response_latency=2)

for cpu in root.system.little_cores:
    cpu.icache = Cache(size="16KiB", assoc=4, tag_latency=3, data_latency=3, response_latency=3)
    cpu.dcache = Cache(size="16KiB", assoc=4, tag_latency=3, data_latency=3, response_latency=3)

# Create and connect L1 crossbar
root.system.l1_xbar = SystemXBar()
for cpu in root.system.big_cores + root.system.little_cores:
    cpu.icache_port = cpu.icache.cpu_side
    cpu.dcache_port = cpu.dcache.cpu_side
    cpu.icache.mem_side = root.system.l1_xbar.cpu_side_ports
    cpu.dcache.mem_side = root.system.l1_xbar.cpu_side_ports

# L2 Cache (Per Cluster)
root.system.big_l2cache = Cache(size="2MiB", assoc=16, tag_latency=4, data_latency=4, response_latency=4)
root.system.little_l2cache = Cache(size="512KiB", assoc=8, tag_latency=5, data_latency=5, response_latency=5)

# Connect L1 to L2
root.system.l1_xbar.mem_side_ports = [root.system.big_l2cache.cpu_side, root.system.little_l2cache.cpu_side]

# Shared L3 Cache
root.system.l3cache = Cache(size="4MiB", assoc=16, tag_latency=6, data_latency=6, response_latency=6)

root.system.big_l2cache.mem_side = root.system.l3cache.cpu_side
root.system.little_l2cache.mem_side = root.system.l3cache.cpu_side
root.system.l3cache.mem_side = root.system.membus.cpu_side_ports

# Memory controller with LPDDR3-1600 MHz
root.system.mem_ctrl = MemCtrl()
root.system.mem_ctrl.dram = LPDDR3_1600_8x8(range=root.system.mem_ranges[0])
root.system.mem_ctrl.port = root.system.membus.mem_side_ports

# Stub for GPU (Mali-T628, not simulated in gem5)
root.system.gpu = "Mali-T628 Stub (Not Simulated)"

# Set up the workload for the system
binary_path = '/opt/GEMM-ArchProfiler/darknet/darknet'
args = ['classifier', 'predict', 'cfg/imagenet1k.data', 'cfg/darknet53.cfg', 'darknet53.weights', 'data/dog.jpg']

# Debugging output
print(f"Binary Path: {binary_path}")
print(f"Arguments: {args}")

# Initialize SEWorkload
root.system.workload = SEWorkload.init_compatible(binary_path)

# Assign the workload to the CPUs
process = Process(pid=100, cmd=[binary_path] + args)
for cpu in root.system.big_cores + root.system.little_cores:
    cpu.workload = process
    cpu.createThreads()

# Connect the system port to the memory bus
root.system.system_port = root.system.membus.cpu_side_ports

# Handle checkpoints
if resume_from_checkpoint and not is_checkpoint_dir_empty(checkpoint_dir):
    print(f"Resuming simulation from checkpoint: {checkpoint_dir}")
    m5.instantiate(checkpoint_dir)
else:
    if not resume_from_checkpoint:
        clear_checkpoint_dir(checkpoint_dir)
        print("Starting fresh simulation...")
        m5.instantiate()

    # Fast-forward logic
    if fast_forward_tick is not None:
        print(f"Fast-forwarding simulation to tick {fast_forward_tick}...")
        exit_event = m5.simulate(fast_forward_tick)
        print(f"Fast-forward completed at tick {m5.curTick()} with reason: {exit_event.getCause()}")
    else:
        print("No fast-forward tick specified. Continuing without fast-forward.")

# Detailed simulation
print("Starting detailed simulation...")
checkpoint_tick = 3700000000000  # Define the tick at which to create a checkpoint
checkpoint_created = False

while True:
    exit_event = m5.simulate()
    print(f"Exited at tick {m5.curTick()} with reason: {exit_event.getCause()}")

    # Create a checkpoint at the specified tick
    if not checkpoint_created and m5.curTick() >= checkpoint_tick:
        print(f"Creating checkpoint at tick {m5.curTick()}...")
        m5.checkpoint(checkpoint_dir)
        print(f"Checkpoint created at: {checkpoint_dir}")
        checkpoint_created = True

    if exit_event.getCause() == "checkpoint":
        print(f"Checkpoint created at tick {m5.curTick()}. Continuing simulation...")
        continue
    else:
        print("Simulation completed.")
        break

print(f"Simulation ended at tick {m5.curTick()} with reason: {exit_event.getCause()}")
