#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <experiment_number>"
    exit 1
fi

# Assign the experiment number to a variable
experiment_number="$1"

# Define the file path
file_path="/discover/nobackup/projects/cmip6/intermediate/current_runs/$experiment_number/I"

# Check if the file exists
if [ -f "$file_path" ]; then
    echo -e "\nMatching I file found: $file_path"

    # Extract information from the second line
    second_line=$(sed -n '2p' "$file_path")

    # Extract the branching_value (AIC value)
    branching_value=$(echo "$second_line" | sed 's/.*=//;s/\..*//' | awk '{gsub(/[[:alpha:]]/, " "); print}' | awk '{print $2}')
    branching_value=$((branching_value - 1))

    # Extract the parent_run_number (text after rsf)
    parent_run_number=$(echo "$second_line" | grep -oP '(?<=rsf)[^.]+' | tr -d '[:space:]')

    # Print the extracted values
    echo -e "   Branching value: $branching_value"
    echo "      Parent run number: $parent_run_number"

    # Define the correct search directory
    search_directory="/discover/nobackup/aherron1/sumfwcmip6/"

    # Search for the appropriate file in the directory
    matching_file=$(ls "$search_directory"sumfw_"${parent_run_number}"_*.gz 2>/dev/null | head -n 1)

    # Check if a matching file is found
    if [ -n "$matching_file" ]; then
        echo -e "\nMatching sumfw file found: $matching_file"

        # Extract values corresponding to the branching year
        echo "  **************************************"
        awk -v branching_year="$branching_value" '$1 == branching_year {printf("        %s %s %s\n", $1, $2, $3)}' <(zcat "$matching_file")
        #awk -v branching_year="$branching_value" '$1 == branching_year {print $1, $2, $3}' <(zcat "$matching_file")
        echo "  **************************************"
    else
        echo "No matching file found in $search_directory"
    fi
else
    echo "File does not exist at $file_path"
fi
