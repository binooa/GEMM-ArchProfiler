## GEM5 Simulator - CPU Configuration(s) - Setup Instructions

---

**Note**: Ensure that you have successfully completed the all previous sections successfully.


### Step 17: Download CPU Configuration Files
```bash
git init
git remote add origin https://github.com/binooa/GEMM-ArchProfiler.git
git config core.sparseCheckout true
echo "cpuconf/" >> .git/info/sparse-checkout
git pull origin main
```
[← GEM5 CPU Configuration Details used for Simulation](gem5cpuconf.md)

[← GEM5 CPU Customization Instructions to change CPU Configuration](gem5cpugeneric.md)

---

## Sample Configuration Files for Intel and ARM Architectures



| Architecture | gem5 CPU Configuration | Remarks |
|----------|----------|----------|
| IntelCorei3_6100U   | [IntelCorei3_6100U Configuration](https://github.com/binooa/GEMM-ArchProfiler/blob/main/cpuconf/IntelCorei3_6100U.py)   | Data 3   |
| Exynos5422   | [Exynos5422 Configuration](https://github.com/binooa/GEMM-ArchProfiler/blob/main/cpuconf/exynos5422.py)   | Data C   |



### GEM5 Simulation - Binary Execution Configuration for Intel and ARM Architectures
This configuration executes a **binary file** within the GEM5 simulation environment. The setup runs the **Darknet-based classifier** to evaluate **GEMM workloads** in CNN-based AI models. It can be replace with Resnet OR Denset.

---

#### **Binary Execution Details**
#### **Binary Path & Execution Arguments**
| Parameter | Value |
|-----------|----------------------------------------------------------|
| **Binary Path** | `/opt/GEMM-ArchProfiler/darknet/darknet` |
| **Execution Mode** | `classifier` |
| **Operation** | `predict` |
| **Dataset Configuration** | `cfg/imagenet1k.data` |
| **Model Configuration** | `cfg/darknet53.cfg` |
| **Pre-trained Weights** | `darknet53.weights` |
| **Input Image** | `data/dog.jpg` |

---


[← Back to Main README](../README.md)