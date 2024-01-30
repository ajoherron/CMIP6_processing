#!/bin/bash

# Gather node data
total_nodes=$(sinfo -h -o "%D")
idle_nodes=$(sinfo -h -t idle -o "%D")
allocated_nodes=$(sinfo -h -t alloc -o "%D")

# Calculate percentages
idle_percentage=$((100 * idle_nodes / total_nodes))
allocated_percentage=$((100 * allocated_nodes / total_nodes))

# Collect total number of jobs
total_jobs=$(squeue -h | wc -l)

# Print results
echo "==========Slurm Node Summary=========="
echo "Total Nodes: $total_nodes"
echo "Number of Idle Nodes: $idle_nodes ($idle_percentage%)"
echo "Allocated Nodes: $allocated_nodes ($allocated_percentage%)"
echo "Total Jobs: $total_jobs"
echo "======================================"
