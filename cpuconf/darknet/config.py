from m5.objects import *
import m5

# Set output directory
m5.core.setOutputDir("/opt/GEMM-ArchProfiler/output")

# Create the system
root = Root(full_system=False)
root.system = System()

# Setup basic parameters
root.system.clk_domain = SrcClockDomain(clock="2GHz", voltage_domain=VoltageDomain())
root.system.mem_mode = 'timing'  # Use timing mode for memory
root.system.mem_ranges = [AddrRange('512MB')]

# Define memory bus
root.system.membus = SystemXBar()

# Setup CPU and interrupt controller
root.system.cpu = TimingSimpleCPU()
root.system.cpu.createInterruptController()

# Connect CPU interrupt ports for X86
root.system.cpu.interrupts[0].pio = root.system.membus.mem_side_ports
root.system.cpu.interrupts[0].int_requestor = root.system.membus.cpu_side_ports
root.system.cpu.interrupts[0].int_responder = root.system.membus.mem_side_ports

# Connect CPU cache ports to memory bus
root.system.cpu.icache_port = root.system.membus.cpu_side_ports
root.system.cpu.dcache_port = root.system.membus.cpu_side_ports

# Setup memory controller with DDR3_1600_8x8 interface
root.system.mem_ctrl = MemCtrl()
root.system.mem_ctrl.dram = DDR3_1600_8x8()
root.system.mem_ctrl.dram.range = root.system.mem_ranges[0]
root.system.mem_ctrl.port = root.system.membus.mem_side_ports

# Set up the workload for the system
binary_path = '/opt/GEMM-ArchProfiler/darknet/darknet'  # Path to the Darknet binary
args = ['classifier', 'predict', 'cfg/imagenet1k.data', 'cfg/darknet53.cfg', 'darknet53.weights', 'data/dog.jpg']

# Initialize the workload with the binary and arguments
root.system.workload = SEWorkload.init_compatible(binary_path)

# Set the CPU process workload
root.system.cpu.workload = Process(cmd=[binary_path] + args)  # Combine binary path and arguments
root.system.cpu.createThreads()

# Connect the system port to the memory bus
root.system.system_port = root.system.membus.cpu_side_ports

# Run simulation
m5.instantiate()
print("Starting simulation...")

exit_event = m5.simulate()  # Run simulation until the C program finishes

print(f"Exiting @ tick {m5.curTick()} because {exit_event.getCause()}")
#print(f"Simulation output written to {m5.options.outdir}")
