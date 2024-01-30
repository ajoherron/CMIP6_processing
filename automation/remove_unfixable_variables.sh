#!/bin/bash

badvars=(CF3hr/ci
    Amon/ci
    */sidmasssi
    */sndmasssnf
    */hfdsn
    */snm
    */rldscs
    */evspsblveg
    */evspsblsoi
    */sispeed
    */hfbasinpadv
    */htovgyre
    */htovovrt
    */sltovgyre
    */sltovovrt
    */mc
    */vsfsit
    */sfdsi)

# Fix exists (can be implemented later)
#3hr/rsdsdiff

# Move to CMOR directory
cd /discover/nobackup/aherron1/CMOR3.3.2 || exit

echo -e "\n==========Deleting unfixable variables==========\n" >>cmor_progress.txt

# Remove all bad variables
for var in "${badvars[@]}"; do
    echo "Deleting: $var" >>cmor_progress.txt
    rm -rf "/discover/nobackup/aherron1/CMOR3.3.2/CMIP6/*/*/*/*/*/$var"
done

echo -e "\n==========Variable deletion complete============\n" >>cmor_progress.txt
