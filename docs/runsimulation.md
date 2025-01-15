## Run Simulation

---

**Note**: Ensure that you have successfully completed the all previous sections successfully.


### Step 18: Run Simualtion
For simulation, GEMM-ArchProfiler uses CNN configurations based on Darknet, DenseNet, and ResNet. You can choose the appropriate network during the execution of the menu-driven run script (`simulate.sh`). Ensure to select the configuration that matches your research requirements.

```bash
cd /opt/GEMM-ArchProfiler
chmod a+x simulate.sh
source simulate.sh

```
**Note**: For simulation, GEMM-ArchProfiler uses CNN configurations based on Darknet, DenseNet, and ResNet. You can choose the appropriate network during the execution of the menu-driven run script (`simulate.sh`). The script executes the simulation as a background process. Ensure to select the configuration that matches your research requirements and check the log files for progress and results.


To view the status of the running process, execute the following command:

```bash
ps -all
```
Check if gem.out is running to ensure the simulation is in progress.

If the Darknet network is chosen, you can view the current simulation state using:
```bash
cat /opt/GEMM-ArchProfiler/output/darknet/darknet_status.log
```

If the Densenet network is chosen, you can view the current simulation state using:
```bash
cat /opt/GEMM-ArchProfiler/output/densenet/densenet_status.log
```

If the Renet network is chosen, you can view the current simulation state using:
```bash
cat /opt/GEMM-ArchProfiler/output/resnet/resnet_status.log
```

## Note

Simulation may take five hours or more, depending on the specifications of the system running the simulation. Ensure sufficient system resources and plan accordingly.

---

[← Back to Main README](../README.md)