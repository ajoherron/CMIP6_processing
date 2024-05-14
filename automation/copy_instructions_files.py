import os
import string
import shutil

##########################################################
### Set base file, base variant, and new variant range ###
##########################################################

# Set base file to copy from
run_format = "E213O3(variant)F40oQ40.json"
base_variant = "f"

# Define range of variants
variant_range = ("g", "t")

############################################
### Automated Instructions File Creation ###
############################################

# Set base file using base variant
base_instructions_file = run_format.replace("(variant)", base_variant)

# Generate a string with all letters (lowercase)
alphabet = string.ascii_lowercase

# Extract the range of letters
start_index = alphabet.index(variant_range[0])
end_index = alphabet.index(variant_range[1])
letters_range = alphabet[start_index : end_index + 1]

# Determine the start value for realization_index based on the position of the first letter in the range
start_value = alphabet.index(variant_range[0]) + 1

# Change directory to location of instructions files
os.chdir("/discover/nobackup/aherron1/exptid")

# Check to see if the base file exists
if not os.path.isfile(base_instructions_file):
    print(f"Base file {base_instructions_file} not found")
    exit(1)

# Print
print(
    f"\nFor base file: {base_instructions_file}, the following instructions files have been created:\n"
)

# Loop through the letters in the given range
for idx, letter in enumerate(letters_range, start=start_value):

    # Create the new file name
    new_instructions_file = run_format.replace("(variant)", letter)
    print(f"    {new_instructions_file}")

    # Copy base file to new file
    shutil.copy(base_instructions_file, new_instructions_file)

    # Update model_id field to match the name of the file (without .json extension)
    model_id = os.path.splitext(new_instructions_file)[0]

    # Update realization_index
    realization_index = str(idx)

    # Read the original file line by line
    with open(new_instructions_file, "r") as f:
        lines = f.readlines()

    # Update the desired fields in the lines
    for i, line in enumerate(lines):
        if '"model_id":' in line:
            lines[i] = f'    "model_id":                     "{model_id}",\n'
        elif '"realization_index":' in line:
            lines[i] = f'    "realization_index":            "{realization_index}",\n'

    # Write the updated lines back to the file
    with open(new_instructions_file, "w") as f:
        f.writelines(lines)
