#!/bin/bash

# Change to nobackup directory
nobackup_directory="/discover/nobackup/aherron1"
cd "$nobackup_directory" || exit

# Initialize counter
missing_years=0

echo -e "\n**********Evaluating all sumfw_* files in nobackup directory**********"

# Loop through all files in the directory matching the format "sumfw_*"
for filename in sumfw_*; do
    # Extract the start and end years from the filename
    start_year=$(echo "$filename" | awk -F'[_-]' '{print $(NF-1)}')
    end_year=$(echo "$filename" | awk -F'[_-]' '{print $NF}')

    # Check if the start and end years are non-empty
    if [ -n "$start_year" ] && [ -n "$end_year" ]; then
        # Print filename, start year, and end year
        echo -e "\n----------Evaluating: $filename----------"
        echo -e "Start Year: $start_year\nEnd Year: $end_year"

        # Loop through the range of years and check if each year is present in the file
        for year in $(seq "$start_year" "$end_year"); do
            if ! grep -q "\b$year\b" "$filename"; then
                echo "  Year $year is missing in the file."
                ((missing_years++))
            fi
        done
    else
        echo "Error: Unable to extract start and end years from the filename $filename."
    fi

    # Print out success message for each file
    if [ "$missing_years" -eq 0 ]; then
        echo -e "All years within the range are present in $filename\nSuccess!\n"
    else
        echo -e "Not all years are present (missing $missing_years years)\nFailure."
    fi
    missing_years=0

done
