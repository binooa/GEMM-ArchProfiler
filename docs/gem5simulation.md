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

[← Back to Main README](../README.md)