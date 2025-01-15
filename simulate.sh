#!/bin/bash

# Function to run the selected program in the background


# Main menu
echo "Select the neural network to run:"
echo "1. Darknet"
echo "2. DenseNet"
echo "3. ResNet"
read -p "Enter your choice [1-3]: " choice

case $choice in
    1)
        echo "You selected Darknet."
        cd /opt/GEMM-ArchProfiler/darknet 
        export GEMM_LOG_DIR="/opt/GEMM-ArchProfiler/output/darknet"        
        nohup /opt/GEMM-ArchProfiler/gem5/build/X86/gem5.opt --outdir=/opt/GEMM-ArchProfiler/gem5_output /opt/GEMM-ArchProfiler/cpuconf/darknet_cpu_config.py > /opt/GEMM-ArchProfiler/output/darknet/darknet_status.log 2>&1 &
        echo "To check the status of execution; execute  'cat  /opt/GEMM-ArchProfiler/output/darknet/darknet_status.log ' "
        ;;
    2)
        echo "You selected DenseNet."
        cd /opt/GEMM-ArchProfiler/darknet
        export GEMM_LOG_DIR="/opt/GEMM-ArchProfiler/output/densenet"            
        nohup /opt/GEMM-ArchProfiler/gem5/build/X86/gem5.opt --outdir=/opt/GEMM-ArchProfiler/gem5_output /opt/GEMM-ArchProfiler/cpuconf/densenet_cpu_config.py > /opt/GEMM-ArchProfiler/output/densenet/densenet_status.log 2>&1 &
        ;;
    3)
        echo "You selected ResNet."
        cd /opt/GEMM-ArchProfiler/darknet
        export GEMM_LOG_DIR="/opt/GEMM-ArchProfiler/output/resnet"               
        nohup /opt/GEMM-ArchProfiler/gem5/build/X86/gem5.opt --outdir=/opt/GEMM-ArchProfiler/gem5_output /opt/GEMM-ArchProfiler/cpuconf/resnet_cpu_config.py > /opt/GEMM-ArchProfiler/output/resnet/resnet_status.log 2>&1 &
        ;;
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac

# Exit the script after starting the background process
echo "Process initialized. Exiting the shell script."

