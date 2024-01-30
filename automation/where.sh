#!/bin/bash

# Check if a directory name is provided as a command line argument
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <directory_name>"
    exit 1
fi

directory_name="$1"
old_archive="/archive/u/rruedy/GISS/*/*$directory_name*"
new_archive="/discover/nobackup/projects/cmip6/intermediate/archive/$directory_name"
acc_directory="/discover/nobackup/projects/cmip6/intermediate/archive/$directory_name/ACC"

# Check if the directory exists in the new archive
if [ -d "$new_archive" ]; then
    echo "Directory '$directory_name' exists in the new archive --> use the ext_project directory for extraction."

    # Check if the ACC directory exists
    if [ -d "$acc_directory" ]; then

        # List files in the ACC directory
        files=("$acc_directory"/JAN*.nc.gz)

        # Check if there are any files
        if [ ${#files[@]} -eq 0 ]; then
            echo "No files found in the ACC directory."
        else
            # Extract years from file names
            years=()
            for file in "${files[@]}"; do
                year=$(echo "$file" | grep -oP '\d{4}' | head -n 1)
                years+=("$year")
            done

            # Find the first and last years
            first_year=$(echo "${years[@]}" | tr ' ' '\n' | sort | head -n 1)
            last_year=$(echo "${years[@]}" | tr ' ' '\n' | sort | tail -n 1)

            echo "First year: $first_year"
            echo "Last year: $last_year"
        fi
    else
        echo "ACC directory does not exist in '$directory_name' in the new archive."
    fi

else
    echo "Directory '$directory_name' does not exist in the new archive."
fi
echo ""

# Check if the directory exists in the old archive
if ls "$old_archive" 1>/dev/null 2>&1; then
    echo "Directory '$directory_name' exists in the old archive --> use the ext_dirac directory for extraction."

    # Find first and last years for old archive
    first_year=$(find "$old_archive" -maxdepth 1 -type f -printf "%f\n" | awk -F_ '{print $2}' | awk -F- '{print $1, $2}' | grep -E '[0-9]' | sort -u | head -n 1 | awk '{print $1}')
    last_year=$(find "$old_archive" -maxdepth 1 -type f -printf "%f\n" | awk -F_ '{print $2}' | awk -F- '{print $1, $2}' | grep -E '[0-9]' | sort -u | tail -n 1 | awk '{print $2}' | cut -d '.' -f 1)

    echo "First year: $first_year"
    echo "Last year: $last_year"

else
    echo "Directory '$directory_name' does not exist in the old archive."
fi
echo ""
