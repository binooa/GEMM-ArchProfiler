import re
import pandas as pd

def parse_gem5_stats(stats_file):
    """Parse GEM5 stats.txt and extract key metrics."""
    metrics = {}
    with open(stats_file, "r") as file:
        for line in file:
            match = re.match(r"(\S+)\s+(\S+)", line)
            if match:
                key, value = match.groups()
                try:
                    metrics[key] = float(value)
                except ValueError:
                    pass
    return metrics

def combine_logs(gemm_log_file, stats_file, output_file):
    """Combine GEMM log with GEM5 statistics."""
    gemm_log = pd.read_csv(gemm_log_file, names=["Tag", "M", "N", "K"])
    gem5_metrics = parse_gem5_stats(stats_file)
    
    # Extract relevant metrics
    runtime = gem5_metrics.get("simSeconds", 0)
    cpi = gem5_metrics.get("system.cpu.cpi", 0)
    mem_bandwidth = gem5_metrics.get("system.mem_ctrl.avgRdBWSys", 0) / 1e6  # MB/s
    total_energy = gem5_metrics.get("system.mem_ctrl.dram.rank0.totalEnergy", 0) + \
                   gem5_metrics.get("system.mem_ctrl.dram.rank1.totalEnergy", 0)
    
    # Add metrics to the GEMM log
    gemm_log["Runtime (s)"] = runtime
    gemm_log["CPI"] = cpi
    gemm_log["Memory Bandwidth (MB/s)"] = mem_bandwidth
    gemm_log["Total Energy (J)"] = total_energy

    gemm_log.to_csv(output_file, index=False)
    print(f"Combined log saved to {output_file}")

# Example usage
combine_logs("gemm_log.csv", "stats.txt", "combined_gemm_log.csv")
