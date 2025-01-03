## darkent CNN library & Customization of CNN library - Setup Instructions

---

**Note**: Ensure that you have successfully completed the gem5 installation as outlined in the previous section before proceeding further.


### Step 6: Clone and Set Up Darknet
## About Darknet

Darknet is an open-source neural network framework written in C and CUDA, designed for speed and flexibility. It is widely used for object detection tasks and supports implementations like YOLO (You Only Look Once). Darknet offers modularity, making it easy to configure and extend for custom use cases, while maintaining high performance for both training and inference on various hardware platforms, including CPUs and GPUs.

Darknet comes with a configuration script that allows the implementation of a wide range of popular CNN architectures. For the testbed, the authors utilized architectures such as Darknet53, DenseNet201, and ResNet152 to demonstrate its versatility and performance.

```bash
git clone https://github.com/pjreddie/darknet
cd darknet
```

### Step 7: Replace Existing Makefile in Darknet Directory
> **Alert**: Make sure your current working directory is set to `/opt/GEMM-ArchProfiler/darknet` before proceeding.
```bash
rm Makefile
wget https://github.com/binooa/GEMM-ArchProfiler/raw/main/Makefile -O Makefile
```


### Step 9: Copy dummy_gpu.c File in Darknet Source Directory
> **Alert**: Make sure your current working directory is set to `/opt/GEMM-ArchProfiler/darknet` before proceeding.
```bash
wget https://github.com/binooa/GEMM-ArchProfiler/raw/main/src/dummy_gpu.c -O src/dummy_gpu.c
```

### Step 10: Make and create executable
> **Alert**: Make sure your current working directory is set to `/opt/GEMM-ArchProfiler/darknet` before proceeding.

```bash
make
```


### Step 11: Download CNN Pretrained Weights
> **Alert**: Make sure your current working directory is set to `/opt/GEMM-ArchProfiler/darknet` before proceeding.
```bash
cd /opt/GEMM-ArchProfiler/darknet
wget https://pjreddie.com/media/files/darknet53.weights
wget https://pjreddie.com/media/files/densenet201.weights
wget https://pjreddie.com/media/files/resnet152.weights
```

#### Check darkent 

### Step 12: Verify the Build
Check if the darknet binary was successfully built by listing the darknet directory:

```bash
ls /opt/GEMM-ArchProfiler/darknet/darknet
```
You should see a file named darknet.

### Step 13: Test Run
Check if the darknet binary was successfully built by listing the darknet directory:

```bash
cd /opt/GEMM-ArchProfiler/darknet
./darknet classifier predict cfg/imagenet1k.data cfg/darknet53.cfg darknet53.weights data/dog.jpg
```
If the binary is built correctly and all files specified in the command line are available, the command will run the classification task using the darknet53 CNN model on the provided image (dog.jpg).
```bash
cd /opt/GEMM-ArchProfiler/darknet
./darknet classifier predict cfg/imagenet1k.data cfg/densenet201.cfg densenet201.weights data/dog.jpg
```
If the binary is built correctly and all files specified in the command line are available, the command will run the classification task using the densenet201 CNN model on the provided image (dog.jpg).

```bash
cd /opt/GEMM-ArchProfiler/darknet
./darknet classifier predict cfg/imagenet1k.data cfg/resnet152.cfg resnet152.weights data/dog.jpg
```
If the binary is built correctly and all files specified in the command line are available, the command will run the classification task using the resnet152 CNN model on the provided image (dog.jpg).

### Step 14: darknet Execution Bug Fixing
> **Alert**: If any, errors are identified during execution due to special characters in configuration files, you can inspect the files using the 'cat' command. Special characters might appear at the end of lines. To remove these characters and make the file readable for Unix-based systems, use the 'dos2unix' command:

```bash
cat -A /opt/GEMM-ArchProfiler/darknet/cfg/imagenet1k.data
dos2unix /opt/GEMM-ArchProfiler/darknet/cfg/imagenet1k.data

cat -A /opt/GEMM-ArchProfiler/darknet/data/imagenet.shortnames.list
dos2unix /opt/GEMM-ArchProfiler/darknet/data/imagenet.shortnames.list

cat -A /opt/GEMM-ArchProfiler/darknet/cfg/darknet53.cfg
dos2unix /opt/GEMM-ArchProfiler/darknet/cfg/darknet53.cfg

cat -A /opt/GEMM-ArchProfiler/darknet/cfg/densenet201.cfg
dos2unix /opt/GEMM-ArchProfiler/darknet/cfg/densenet201.cfg

cat -A /opt/GEMM-ArchProfiler/darknet/cfg/resnet152.cfg
dos2unix /opt/GEMM-ArchProfiler/darknet/cfg/resnet152.cfg
```

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


### Step 15: Download CPU Configuration Files
```bash
git init
git remote add origin https://github.com/binooa/GEMM-ArchProfiler.git
git config core.sparseCheckout true
echo "cpuconf/" >> .git/info/sparse-checkout
git pull origin main
```



[← Back to Main README](../README.md)