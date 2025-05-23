import os
import shutil
from m5.objects import *
import m5

# Set output directory
m5.core.setOutputDir("/opt/GEMM-ArchProfiler/output/IntelCorei7_11370H")

# Checkpoint directory
checkpoint_dir = "/opt/GEMM-ArchProfiler/output/checkpoints/IntelCorei7_11370H"

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

# Set clock to 3.3 GHz to match base clock of i7-11370H
root.system.clk_domain = SrcClockDomain(clock="3.3GHz", voltage_domain=VoltageDomain())
root.system.mem_mode = 'timing'
root.system.mem_ranges = [AddrRange('16GiB')]  # Assume 16GB DDR4

# System bus
root.system.membus = SystemXBar()

# 4-core out-of-order CPU model (Hyper-Threading not modeled in gem5)
root.system.cpu = [O3CPU(cpu_id=i) for i in range(4)]

# Interrupt controllers and caches
for cpu in root.system.cpu:
    cpu.createInterruptController()
    cpu.interrupts[0].pio = root.system.membus.mem_side_ports
    cpu.interrupts[0].int_requestor = root.system.membus.cpu_side_ports

    # L1 Caches: 32 KB I-cache, 48 KB D-cache (approximation)
    cpu.icache = Cache(size="32KiB", assoc=8, tag_latency=2, data_latency=2, response_latency=2)
    cpu.dcache = Cache(size="48KiB", assoc=12, tag_latency=2, data_latency=2, response_latency=2)

    cpu.icache_port = cpu.icache.cpu_side
    cpu.dcache_port = cpu.dcache.cpu_side
    cpu.icache.mem_side = root.system.membus.cpu_side_ports
    cpu.dcache.mem_side = root.system.membus.cpu_side_ports

# L2 Cache: Private 1.25 MiB per core
root.system.l2 = [Cache(size="1.25MiB", assoc=16, tag_latency=4, data_latency=4, response_latency=4)
                  for _ in range(4)]
for i in range(4):
    root.system.cpu[i].l2cache = root.system.l2[i]
    root.system.cpu[i].dcache.mem_side = root.system.l2[i].cpu_side
    root.system.l2[i].mem_side = root.system.membus.cpu_side_ports

# Shared L3 cache: 12 MiB
root.system.l3cache = Cache(size="12MiB", assoc=24, tag_latency=6, data_latency=6, response_latency=6)
for l2 in root.system.l2:
    l2.mem_side = root.system.l3cache.cpu_side
root.system.l3cache.mem_side = root.system.membus.cpu_side_ports

# Memory controller: Approximate LPDDR4x/DDR4
root.system.mem_ctrl = MemCtrl()
root.system.mem_ctrl.dram = DDR4_2400_8x8(range=root.system.mem_ranges[0])  # Approximation
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
