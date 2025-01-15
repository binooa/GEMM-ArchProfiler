import os
import shutil
from m5.objects import *
import m5

# Set output directory
m5.core.setOutputDir("/opt/GEMM-ArchProfiler/output/darknet")

# Checkpoint directory
checkpoint_dir = "/opt/GEMM-ArchProfiler/output/checkpoints/darknet"

# Options
resume_from_checkpoint = False  # Set to True to resume from a saved checkpoint
fast_forward_tick = None   # Set the tick to fast-forward = 3700000000000 if resuming from a checkpoint, otherwise None

# Function to check if the checkpoint directory is empty
def is_checkpoint_dir_empty(dir_path):
    return not os.listdir(dir_path)  # Returns True if the directory is empty

# Function to clear the checkpoint directory
def clear_checkpoint_dir(dir_path):
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
        print(f"Cleared existing checkpoint directory: {dir_path}")

# Create the system
root = Root(full_system=False)
root.system = System()

# Setup basic parameters
root.system.clk_domain = SrcClockDomain(clock="2GHz", voltage_domain=VoltageDomain())
root.system.mem_mode = 'timing'  # Use timing mode for O3CPU
root.system.mem_ranges = [AddrRange('4GiB')]

# Define memory bus
root.system.membus = SystemXBar()

# Setup 1 O3CPU core
root.system.cpu = O3CPU(cpu_id=0)

# Create interrupt controller for the CPU (X86-specific)
root.system.cpu.createInterruptController()
root.system.cpu.interrupts[0].pio = root.system.membus.mem_side_ports
root.system.cpu.interrupts[0].int_requestor = root.system.membus.cpu_side_ports

# L1 Caches
root.system.cpu.icache = Cache(
    size="32KiB",
    assoc=8,
    tag_latency=2,
    data_latency=2,
    response_latency=2,
    mshrs=16,
    tgts_per_mshr=8,
)
root.system.cpu.dcache = Cache(
    size="32KiB",
    assoc=8,
    tag_latency=2,
    data_latency=2,
    response_latency=2,
    mshrs=16,
    tgts_per_mshr=8,
)

# Connect L1 caches to the CPU
root.system.cpu.icache_port = root.system.cpu.icache.cpu_side
root.system.cpu.dcache_port = root.system.cpu.dcache.cpu_side

# Create and connect L1 crossbar
root.system.l1_xbar = SystemXBar()
root.system.cpu.icache.mem_side = root.system.l1_xbar.cpu_side_ports
root.system.cpu.dcache.mem_side = root.system.l1_xbar.cpu_side_ports

# L2 Cache
root.system.l2cache = Cache(
    size="256KiB",
    assoc=4,
    tag_latency=4,
    data_latency=4,
    response_latency=4,
    mshrs=32,
    tgts_per_mshr=16,
)
root.system.l1_xbar.mem_side_ports = root.system.l2cache.cpu_side

# L3 Cache
root.system.l3cache = Cache(
    size="8MiB",
    assoc=16,
    tag_latency=6,
    data_latency=6,
    response_latency=6,
    mshrs=64,
    tgts_per_mshr=32,
)
root.system.l2cache.mem_side = root.system.l3cache.cpu_side
root.system.l3cache.mem_side = root.system.membus.cpu_side_ports

# Memory controller wrapping DDR3 memory
root.system.mem_ctrl = MemCtrl()
root.system.mem_ctrl.dram = DDR3_1600_8x8(range=root.system.mem_ranges[0])
root.system.mem_ctrl.port = root.system.membus.mem_side_ports

# Set up the workload for the system
binary_path = '/opt/GEMM-ArchProfiler/darknet/darknet'
args = ['classifier', 'predict', 'cfg/imagenet1k.data', 'cfg/darknet53.cfg', 'darknet53.weights', 'data/dog.jpg']

# Debugging output
print(f"Binary Path: {binary_path}")
print(f"Arguments: {args}")

# Initialize SEWorkload
root.system.workload = SEWorkload.init_compatible(binary_path)

# Assign the workload to the CPU
process = Process(pid=100, cmd=[binary_path] + args)
root.system.cpu.workload = process
root.system.cpu.createThreads()

# Connect the system port to the memory bus
root.system.system_port = root.system.membus.cpu_side_ports

# Handle checkpoints
if resume_from_checkpoint and not is_checkpoint_dir_empty(checkpoint_dir):
    print(f"Resuming simulation from checkpoint: {checkpoint_dir}")
    m5.instantiate(checkpoint_dir)
else:
    if not resume_from_checkpoint:
        clear_checkpoint_dir(checkpoint_dir)  # Clear previous checkpoints if any
        print("Starting fresh simulation...")
        m5.instantiate()

    # Fast-forward logic
    if fast_forward_tick is not None:  # Correctly check if fast_forward_tick is set
        print(f"Fast-forwarding simulation to tick {fast_forward_tick}...")
        exit_event = m5.simulate(fast_forward_tick)
        print(f"Fast-forward completed at tick {m5.curTick()} with reason: {exit_event.getCause()}")
    else:
        print("No fast-forward tick specified. Continuing without fast-forward.")

# Detailed simulation
print("Starting detailed simulation...")
checkpoint_tick = 3700000000000  # Define the tick at which to create a checkpoint
checkpoint_created = False  # Track if the checkpoint is created

while True:
    exit_event = m5.simulate()
    print(f"Exited at tick {m5.curTick()} with reason: {exit_event.getCause()}")

    # Create a checkpoint at the specified tick
    if not checkpoint_created and m5.curTick() >= checkpoint_tick:
        print(f"Creating checkpoint at tick {m5.curTick()}...")
        m5.checkpoint(checkpoint_dir)
        print(f"Checkpoint created at: {checkpoint_dir}")
        checkpoint_created = True  # Ensure the checkpoint is created only once

    if exit_event.getCause() == "checkpoint":
        print(f"Checkpoint created at tick {m5.curTick()}. Continuing simulation...")
        continue
    else:
        print("Simulation completed.")
        break

print(f"Simulation ended at tick {m5.curTick()} with reason: {exit_event.getCause()}")