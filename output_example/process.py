import re
import pandas as pd


def parse_gemm_layers(layers_file):
    """Parse GEMM layers from gemm_calls.txt."""
    layers = []
    with open(layers_file, "r") as file:
        for line in file:
            line = line.strip()
            if line.startswith("GEMM Layer:"):
                # Extract GEMM layer details
                match = re.search(r"M:\s*(\d+),\s*N:\s*(\d+),\s*K:\s*(\d+)", line)
                if match:
                    M, N, K = map(int, match.groups())
                    layers.append((M, N, K))
    return layers


def parse_stats_file(stats_file):
    """Split stats.txt into individual blocks."""
    with open(stats_file, "r") as file:
        content = file.read()
    blocks = re.split(r"---------- End Simulation Statistics\s+----------", content)
    return [block.strip() for block in blocks if block.strip()]


def extract_units_and_values(block):
    """Extract stats and units from a stats block."""
    stats_data = {}
    units = {}
    stat_pattern = re.compile(r"([\w\.:]+)\s+([\d\.Ee+-]+)\s+(.*)")

    for line in block.splitlines():
        match = stat_pattern.match(line.strip())
        if match:
            parameter_name, value, unit = match.groups()
            stats_data[parameter_name] = float(value)
            units[parameter_name] = unit

    return stats_data, units


def calculate_metrics(stats, M, N, K):
    """Calculate the requested metrics."""
    metrics = {}

    # Calculate FLOPs
    scalar_fp_ops = stats.get("system.cpu.commitStats0.numFpInsts", 0)
    vector_fp_ops = stats.get("system.cpu.commitStats0.numVecInsts", 0)
    sim_seconds = stats.get("simSeconds", 1e-9)  # Avoid division by zero

    # Assuming each vector FP operation performs 4 FLOPs
    vector_width = 4  # Adjust based on your architecture
    total_flops = scalar_fp_ops + (vector_fp_ops * vector_width)
    flop_rate = total_flops / sim_seconds  # FLOP rate (FLOPs/s)

    runtime_seconds = stats.get("simSeconds", 0)
    cpi = stats.get("system.cpu.cpi", 0)

    sim_frequency = 1e12  # 1 THz (ticks/second) as default in GEM5
    clock_period_ticks = stats.get("system.clk_domain.clock", 1)  # Default to 1 if not found
    clock_frequency_hz = sim_frequency / clock_period_ticks
    mem_clock_mhz = clock_frequency_hz / 1e6  # Convert Hz to MHz

    mem_clock = mem_clock_mhz
    l1_cache = 32  # kB (static assumption)
    l2_cache = 256  # kB (static assumption)
    l3_cache = 3  # MB (static assumption)
    avg_read_bw = stats.get("system.mem_ctrl.avgRdBWSys", 0) / 1e6  # MB/s

    # DRAM energy
    dram_energy = stats.get("system.mem_ctrl.dram.rank0.totalEnergy", 0) + stats.get(
        "system.mem_ctrl.dram.rank1.totalEnergy", 0
    )

    # CPU energy calculation
    cpu_residency_ticks = stats.get("system.cpu.power_state.pwrStateResidencyTicks::ON", 0)
    cpu_clock = stats.get("system.clk_domain.clock", 1)  # In ticks
    cpu_power = 50  # Assume a default CPU power consumption in Watts
    cpu_energy = (cpu_residency_ticks / cpu_clock) * cpu_power

    # Total energy and power
    total_energy = dram_energy + cpu_energy
    total_power = total_energy / runtime_seconds if runtime_seconds else 0

    # Compute derived metrics
    metrics["Layer"] = f"GEMM Layer ({M}, {N}, {K})"
    metrics["M"] = M
    metrics["N"] = N
    metrics["K"] = K
    metrics["L1 Cache [kB]"] = l1_cache
    metrics["L2 Cache [kB]"] = l2_cache
    metrics["L3 Cache [MB]"] = l3_cache
    metrics["Memory Clock [MHz]"] = mem_clock
    metrics["Mean Runtime (RDTSC) [s]"] = runtime_seconds
    metrics["Mean CPI"] = cpi
    metrics["Mean DP [MFLOP/s]"] = flop_rate / 1e6
    metrics["Memory Bandwidth [MB/s]"] = avg_read_bw
    metrics["Energy [J]"] = total_energy
    metrics["Power [W]"] = total_power
    metrics["Operational Intensity"] = total_flops / avg_read_bw if avg_read_bw else 0
    metrics["MaxFLOPS"] = total_flops

    return metrics


def generate_csv(layers_file, stats_file, output_csv):
    """Generate CSV combining GEMM parameters and statistics."""
    # Parse GEMM layers
    layers = parse_gemm_layers(layers_file)

    print(f"Found {len(layers)} GEMM layers.")  # Debugging information

    # Parse stats file into blocks
    stats_blocks = parse_stats_file(stats_file)

    print(f"Found {len(stats_blocks)} stats blocks.")  # Debugging information

    # Ensure the number of stats blocks matches or exceeds GEMM layers
    if len(stats_blocks) < len(layers):
        print(
            f"Warning: {len(layers) - len(stats_blocks)} GEMM layers do not have corresponding stats blocks."
        )
        layers = layers[: len(stats_blocks)]  # Truncate layers to match stats blocks

    # Combine metrics for each layer
    combined_metrics = []
    for (M, N, K), block in zip(layers, stats_blocks):
        stats_data, _ = extract_units_and_values(block)
        metrics = calculate_metrics(stats_data, M, N, K)
        combined_metrics.append(metrics)

    # Convert to DataFrame and save as CSV
    df = pd.DataFrame(combined_metrics)
    df.to_csv(output_csv, index=False)
    print(f"CSV file saved to {output_csv}")


# Example usage
generate_csv("gemm_calls.txt", "stats.txt", "gemm_metrics.csv")
