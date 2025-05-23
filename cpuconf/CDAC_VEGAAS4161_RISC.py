import os
import shutil
from m5.objects import *
import m5

# Set output directory
m5.core.setOutputDir("/opt/GEMM-ArchProfiler/output/CDAC_VEGAAS4161_RISC")

# Checkpoint directory
checkpoint_dir = "/opt/GEMM-ArchProfiler/output/checkpoints/CDAC_VEGAAS4161_RISC"

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

# Set up the system
root = Root(full_system=False)
root.system = System()

# Clock and voltage domain (typical estimate)
root.system.clk_domain = SrcClockDomain(clock="1.5GHz", voltage_domain=VoltageDomain())
root.system.mem_mode = 'timing'
root.system.mem_ranges = [AddrRange('4GiB')]

# System bus
root.system.membus = SystemXBar()

# Quad-core RV64 Out-of-Order processor model
root.system.cpu = [O3CPU(cpu_id=i) for i in range(4)]

# Interrupt controller and cache setup
for cpu in root.system.cpu:
    cpu.createInterruptController()

    # L1 Instruction and Data Cache
    cpu.icache = Cache(size="32KiB", assoc=4, tag_latency=2, data_latency=2, response_latency=2)
    cpu.dcache = Cache(size="32KiB", assoc=4, tag_latency=2, data_latency=2, response_latency=2)
    
    cpu.icache_port = cpu.icache.cpu_side
    cpu.dcache_port = cpu.dcache.cpu_side
    
    cpu.icache.mem_side = root.system.membus.cpu_side_ports
    cpu.dcache.mem_side = root.system.membus.cpu_side_ports

# Coherent interconnect simulated via a crossbar
root.system.l1_xbar = SystemXBar()
for cpu in root.system.cpu:
    cpu.icache.mem_side = root.system.l1_xbar.cpu_side_ports
    cpu.dcache.mem_side = root.system.l1_xbar.cpu_side_ports

# Shared Configurable L2 Cache
root.system.l2cache = Cache(size="1MiB", assoc=8, tag_latency=4, data_latency=4, response_latency=4)
root.system.l1_xbar.mem_side_ports = root.system.l2cache.cpu_side
root.system.l2cache.mem_side = root.system.membus.cpu_side_ports

# Memory Controller (LPDDR4 assumed)
root.system.mem_ctrl = MemCtrl()
root.system.mem_ctrl.dram = DDR4_2400_8x8(range=root.system.mem_ranges[0])
root.system.mem_ctrl.port = root.system.membus.mem_side_ports

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
