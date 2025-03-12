# GEMM-ArchProfiler - Sample Outputs

## Log Files after Simulation

After the completion of the simulation, two important output files will be generated:

1. **`gemm_calls.txt`**  
   - Contains details of each GEMM call in the CNN simulation.
   - Logs key parameters such as **M**, **N**, and **K** for every GEMM operation.

2. **`stats.txt`**  
   - Contains the detailed simulation logs from the `gem5` simulation.
   - Includes hardware performance metrics such as cache behavior, memory usage, and execution latencies.


### Sample Log Files

You can find a sample gemm_calls.txt [here](../output_example/gemm_calls.txt).
You can find a sample stats.txt [here](../output_example/stats.txt).

## Output File after Processing Simlation results

After successful execution of data processing script, the script will generate a gemm_metrics.csv file in the same directory. This file contains a comprehensive analysis of the GEMM operations, including key performance metrics derived from the logs.

### Sample Output file

You can find a sample gemm_metrics.csv [here](../output_example/gemm_metrics.csv).
