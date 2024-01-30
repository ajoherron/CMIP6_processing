#!/bin/bash

# Move to CMOR directory
cmor_directory="/discover/nobackup/aherron1/CMOR3.3.2"
cd "$cmor_directory" || exit
echo -e "\n**********Testing all runs in CMOR3.3.2**********\n"

# Use find command to locate directories following correct run structure
find "$cmor_directory" -type d -name "r*i*p*f*" -print |

    # Loop through each directory matching above format
    while IFS= read -r directory; do

        # Highlight the run being tested
        echo "----------Testing run: $directory----------"

        # Run the additional find command for each directory
        #find "$directory" -mindepth 5 ! -name "*_gn_*nc"

        # Calculate how many files are incorrect
        file_count=$(find "$directory" -mindepth 5 ! -name "*_gn_*nc" -print | wc -l)
        echo "Number of faulty files: $file_count"

        # Check if the file count is zero or not
        if [ "$file_count" -eq 0 ]; then
            echo -e "CMORization process successful!\n"
        else
            echo -e "CMORization process failure.\n"
        fi
    done
