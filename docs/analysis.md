## Analyze Simulation Results

---

**Note**: Ensure that you have successfully completed the all previous sections successfully.


## Output Files

After the completion of the simulation, two important output files will be generated:

1. **`gemm_calls.txt`**  
   - Contains details of each GEMM call in the CNN simulation.
   - Logs key parameters such as **M**, **N**, and **K** for every GEMM operation.

2. **`stats.txt`**  
   - Contains the detailed simulation logs from the `gem5` simulation.
   - Includes hardware performance metrics such as cache behavior, memory usage, and execution latencies.


### Sample Files

You can find a sample gemm_calls.txt [here](../output_example/gemm_calls.txt).
You can find a sample stats.txt [here](../output_example/stats.txt).

### Output Directory

All output files are saved in directories corresponding to the selected CNN network configuration:

- **DenseNet:** `/opt/GEMM-ArchProfiler/output/densenet/`
- **Darknet:** `/opt/GEMM-ArchProfiler/output/darknet/`
- **ResNet:** `/opt/GEMM-ArchProfiler/output/resnet/`

The output directory depends on the network chosen during the simulation process (`DenseNet`, `Darknet`, or `ResNet`).

### Key Notes

- **`gemm_calls.txt`** is useful for analyzing GEMM operations with specific matrix parameters (**M**, **N**, **K**) used in the CNN simulation.  
- **`stats.txt`** provides insights into the performance metrics of the simulated architecture, such as cache utilization, memory bandwidth, and latency.  

- Ensure to navigate to the appropriate directory to access the output files based on the simulation network selected.

### Step 18: Anaylyze Simulation Results

To run analysis, make sure the `process.py` file is copied to the appropriate directory:

```bash
cp /opt/GEMM-ArchProfiler/process.py /opt/GEMM-ArchProfiler/output/<network>/
```
Replace <network> with the selected network folder:
DenseNet: /opt/GEMM-ArchProfiler/output/densenet/
Darknet: /opt/GEMM-ArchProfiler/output/darknet/
ResNet: /opt/GEMM-ArchProfiler/output/resnet/

For example, if you are analyzing the simulation for DenseNet:
```bash
cp /opt/GEMM-ArchProfiler/process.py /opt/GEMM-ArchProfiler/output/densenet/
```
Once the file is copied, you can execute the analysis scripts to generate insights based on the simulation logs.

Navigate to the output directory of the selected network:
```bash
cd /opt/GEMM-ArchProfiler/output/<network>/
```
Replace <network> with the selected network folder:
DenseNet: /opt/GEMM-ArchProfiler/output/densenet/
Darknet: /opt/GEMM-ArchProfiler/output/darknet/
ResNet: /opt/GEMM-ArchProfiler/output/resnet/

Run the process.py script to analyze the simulation outputs:
```bash
python3 process.py
```
After successful execution, the script will generate a gemm_metrics.csv file in the same directory. This file contains a comprehensive analysis of the GEMM operations, including key performance metrics derived from the logs.

### Sample Output file

You can find a sample gemm_metrics.csv [here](../output_example/gemm_metrics.csv).


[← Back to Main README](../README.md)