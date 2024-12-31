#!/bin/bash

# Function to run the specified program
run_program() {
    local network=$1
    local config=$2
    local output_dir="/opt/GEMM-ArchProfiler/output/${network}"
    local script_path="/opt/GEMM-ArchProfiler/cpuconf/${network}/${config}.py"
    
    echo "Running ${network} with configuration ${config}..."
    /opt/GEMM-ArchProfiler/gem5/gem5/build/X86/gem5.opt --outdir=${output_dir} ${script_path}
    echo "Execution completed for ${network} with ${config}."
}

# Main menu function
menu() {
    echo "Select a neural network to run:"
    echo "1. Darknet"
    echo "2. DenseNet"
    echo "3. ResNet"
    echo "4. Exit"
    read -p "Enter your choice [1-4]: " choice

    case $choice in
        1)
            echo "You selected Darknet."
            run_program "darknet" "samsung_exynos"
            run_program "darknet" "x86_intel_skylake_i3"
            ;;
        2)
            echo "You selected DenseNet."
            run_program "densenet" "samsung_exynos"
            run_program "densenet" "x86_intel_skylake_i3"
            ;;
        3)
            echo "You selected ResNet."
            run_program "resnet" "samsung_exynos"
            run_program "resnet" "x86_intel_skylake_i3"
            ;;
        4)
            echo "Exiting the program. Goodbye!"
            exit 0
            ;;
        *)
            echo "Invalid choice. Please select a valid option."
            ;;
    esac
}

# Loop to display the menu until the user exits
while true; do
    menu
    echo ""
done
