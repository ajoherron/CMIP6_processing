#!/bin/ksh

# Move to nobackup directory
cd /discover/nobackup/aherron1/ || exit

# Set directory path for sumfw
sumfw_dir="/discover/nobackup/aherron1/sumfwcmip6"

# Loop through all sumfw files
for file in sumfw_*; do
    echo "Zipping file: $file"
    gzip "$file"

    # Move the zipped file to sumfwcmip6
    echo "Moving $file to $sumfw_dir"
    mv "$file.gz" "$sumfw_dir"
done
