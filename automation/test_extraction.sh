#!/bin/bash

# Constants
FILES1_DIR="/discover/nobackup/aherron1/files1"
FILES2_DIR="/discover/nobackup/aherron1/files2"

# Check if the number of arguments is correct
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <pattern>"
    exit 1
fi

# Function to check files in a directory
check_files() {
    local directory="$1"
    local pattern="$2"

    # Array to store file paths
    files=()

    # Use find command to search for files matching the pattern in the specified directory
    while IFS= read -r file; do
        # Add file path to the array
        files+=("$file")
    done < <(find "$directory" -type f -name "$pattern" | sort)

    # Loop through sorted files
    for file in "${files[@]}"; do

        # Potentially more reliable option
        # Check if the output of qdf contains "not found"
        #if qdf "$file" | grep -q "not found"; then

        # Faster option
        # Check if the file size reported by du is 0
        if [ "$(du -s "$file" | awk '{print $1}')" -eq 0 ]; then

            echo -e "\n!!!!!!!!!!!!!!!\n!!! WARNING !!!\n!!!!!!!!!!!!!!!"
            echo -e "\nFile '$file' is empty"
        fi

    done
}

# Call the function with command-line argument for the pattern for files1 directory
echo -e "\nChecking files in $FILES1_DIR..."
time check_files "$FILES1_DIR" "$1"

# Call the function with command-line argument for the pattern for files2 directory
echo -e "\nChecking files in $FILES2_DIR..."
time check_files "$FILES2_DIR" "$1"
