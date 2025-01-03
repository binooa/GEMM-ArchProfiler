## GEMM Algorithm(s) Implementation in Customised darknet CNN library - Setup Instructions

---

**Note**: Ensure that you have successfully completed the gem5 installation and  darknet CNN library & Customization of darknet CNN library as outlined in the previous sections before proceeding further.

### Step 15: Replace Existing gemm.c File in Darknet Source Directory
> **Alert**: Make sure your current working directory is set to `/opt/GEMM-ArchProfiler/darknet` before proceeding.
```bash
cd /opt/GEMM-ArchProfiler/darknet/
rm src/gemm.c
wget https://github.com/binooa/GEMM-ArchProfiler/raw/main/src/gemm.c -O src/gemm.c
```

### Step 16: ReMake and create executable
> **Alert**: Make sure your current working directory is set to `/opt/GEMM-ArchProfiler/darknet` before proceeding.

```bash
cd /opt/GEMM-ArchProfiler/darknet
make clean
make
```

---

[← Back to Main README](../README.md)