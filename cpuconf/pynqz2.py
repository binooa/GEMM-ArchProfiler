import os
import shutil
from m5.objects import *
import m5

# Set output directory
m5.core.setOutputDir("/opt/GEMM-ArchProfiler/output/pynqz2")

# Checkpoint directory
checkpoint_dir = "/opt/GEMM-ArchProfiler/output/checkpoints/pynqz2"

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

# Clock and Voltage domain (PYNQ-Z2: Cortex-A9 runs up to ~650MHz)
root.system.clk_domain = SrcClockDomain(clock="650MHz", voltage_domain=VoltageDomain())

# Memory mode and address range
root.system.mem_mode = 'timing'
root.system.mem_ranges = [AddrRange('512MB')]  # PYNQ-Z2 typically has 512MB DDR memory

# Memory bus
root.system.membus = SystemXBar()

# Cortex-A9 is an in-order CPU; use MinorCPU as an approximation
root.system.cpu = [MinorCPU(cpu_id=i) for i in range(2)]  # Dual-core Cortex-A9

# Interrupt controller setup
for cpu in root.system.cpu:
    cpu.createInterruptController()
    cpu.interrupts[0].pio = root.system.membus.mem_side_ports
    cpu.interrupts[0].int_requestor = root.system.membus.cpu_side_ports

# L1 caches (32 KB I-cache and 32 KB D-cache per core)
for cpu in root.system.cpu:
    cpu.icache = Cache(size="32KiB", assoc=4, tag_latency=2, data_latency=2, response_latency=2)
    cpu.dcache = Cache(size="32KiB", assoc=4, tag_latency=2, data_latency=2, response_latency=2)
    cpu.icache_port = cpu.icache.cpu_side
    cpu.dcache_port = cpu.dcache.cpu_side

# L1 to shared bus
root.system.l1_xbar = SystemXBar()
for cpu in root.system.cpu:
    cpu.icache.mem_side = root.system.l1_xbar.cpu_side_ports
    cpu.dcache.mem_side = root.system.l1_xbar.cpu_side_ports

# Shared L2 cache (512 KB)
root.system.l2cache = Cache(size="512KiB", assoc=8, tag_latency=4, data_latency=4, response_latency=4)
root.system.l1_xbar.mem_side_ports = root.system.l2cache.cpu_side
root.system.l2cache.mem_side = root.system.membus.cpu_side_ports

# Memory controller with realistic LPDDR2 for PYNQ-Z2
root.system.mem_ctrl = MemCtrl()
root.system.mem_ctrl.dram = DDR3_1600_8x8(range=root.system.mem_ranges[0])  # Closest available
root.system.mem_ctrl.port = root.system.membus.mem_side_ports

# No GPU in gem5 simulation for PYNQ-Z2, so leave it out or use a stub comment
root.system.gpu = "Not simulated (Cortex-A9 on PYNQ-Z2 does not include a programmable GPU)"

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
