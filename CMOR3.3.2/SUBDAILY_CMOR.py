# $1 run name
# $2 year start
# $3 year end
# $4 optional compression argument "compress"

# Standard imports
import sys
import os
import subprocess
import glob
import time


# Export path
def set_path():
    """
    Set PATH environment variable for subprocesses
    """
    username = subprocess.check_output("whoami", shell=True, text=True).strip()
    path1 = f"/discover/nobackup/{username}/CMOR3.3.2"
    path2 = f"/discover/nobackup/{username}/proc_cmip6"

    # Modify PATH environment variable
    os.environ["PATH"] = f'{path1}:{path2}:{os.environ["PATH"]}'


# Ensure sufficient CLA
def check_args():
    """
    Must pass CLA or script exits gracefully
    """
    # Check if the correct number of command line arguments are provided
    if len(sys.argv) < 4:
        print("Usage: python auto_cmorall_subdd.py runname startyear endyear compress")
        print('Optional 5th argument "compress" to turn on compression')
        sys.exit(1)


# dynamic function, any res ## check for accuracy
def process_cmor_data_chunk(
    master, runname, startyear, endyear, tres, num_pday, tres_ychunk, YN_6hrL
):
    """
    tres output
    Usually done in tres_ychunk year increments (e.g. 1850 - 1874)

    master = master cmor script
    runname = internal simulation name
    starty = first year being cmored
    endy = last year being cmored
    tres = time resolution (str) (e.g. 3hr)
    num_pday = number of times per day (e.g. 3hr = 8 num_pday)
    tres_ychunk = time resolution max years proc at once (int)
    YN_6hrL = Binary Y/N for whether processing 6hrL data (different # command line args)
    """

    # Extract years info from start/end year to get processing chunks
    ## Need to process data in chunks due to how much data the fortran programs are able to ingest at once
    ### Dependent upon number of bytes in a record (e.g. daily data with pressure levels > 2d daily data, so less years can be processed at once for pressure level data)
    numyears = endyear + 1 - startyear
    numblocks = int(numyears / tres_ychunk // 1)  # tres_ychunk yr blocks for tres data

    # If the time resolution chunk exceeds the total number of years passed, then just process the entire period passed
    if numblocks == 0:
        y1 = startyear
        y2 = endyear
        num_data_points = (
            (endyear + 1 - startyear) * num_pday * 365
        )  # numyears*timesinday*daysinyear (number data points per chunk)
        numblocks = 1  # reset numblocks to one, so only one iteration is processed (full period)
    # Otherwise process in blocks of N year periods dependent upon # bytes per record, get number of data points per chunk
    else:
        y1 = startyear
        y2 = startyear + tres_ychunk - 1
        num_data_points = tres_ychunk * num_pday * 365  # numyears*timesinday*daysinyear

    # Run CMOR script for time blocks
    for i in range(numblocks):
        # Select syntax based on whether processing 6hrL or not
        if YN_6hrL.lower() == "y":
            cmor_command = f"{master} {runname} {y2} {startyear}"
        else:
            cmor_command = (
                f"{master} {runname} {tres} {num_data_points} {y1} {y2} {startyear}"
            )
        print(f"----- Starting:  {cmor_command} -----")

        # Adding error handling to subprocess
        try:
            subprocess.check_call(cmor_command, shell=True)
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e}")

        # Update chunk
        y1 = y2 + 1
        y2 = y1 + tres_ychunk - 1

    # Do the remainder (if any)
    if y1 < endyear:
        y2 = endyear  # Since less than tres_ychunk years here, cap at end year
        num_data_points = (
            # num_years * times_per_day *days_per_year
            (y2 + 1 - y1)
            * num_pday
            * 365
        )
        if YN_6hrL.lower() == "y":
            cmor_command = f"{master} {runname} {y2} {startyear}"
        else:
            cmor_command = (
                f"{master} {runname} {tres} {num_data_points} {y1} {y2} {startyear}"
            )
        print(f"----- Starting:  {cmor_command} -----")

        # Adding error handling to subprocess
        try:
            subprocess.check_call(cmor_command, shell=True)
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e}")


# Option compression add-on
def compress_all(compress_binary):
    """
    Option to compress all the NetCDF files
    produced by subdaily CMOR process.
    Will use the most recent file by timestamp
    to determine the run that needs to be compressed.
    """

    if compress_binary:
        print("Compressing NetCDF files with level 1 compression...")

        # Get a list of all files matching the pattern
        cmip6_file_list = glob.glob("CMIP6/*/*/*/*/*/*/*/*/*/*_gn_*.nc")

        # Check if any files were found
        if cmip6_file_list:
            # Get the latest file based on modification time (to pick out the latest run)
            latest_file = max(cmip6_file_list, key=os.path.getmtime)
            subdirs = latest_file.split("/")
            print("Compressing files...")
            for ncfile in glob.glob(
                f"{subdirs[0]}/{subdirs[-10]}/{subdirs[-9]}/{subdirs[-8]}/{subdirs[-7]}/{subdirs[-6]}/*/*/*/*/*_gn_*nc"
            ):
                compressit = f"ncks -4 -L 1 -h -O {ncfile} {ncfile}"
                subprocess.call(compressit, shell=True)
                print(compressit)

            print("File compression finished! :)")

        else:
            print("No files found in the specified directory pattern.")


# Set up execution of processing
def run():
    # Record the start time
    start_time = time.time()

    # Make sure command line arguments are correctly used
    check_args()

    # Extract mandatory command line arguments
    master = "master_cmor3.ksh"  # Setting this as constant from now on (still can be changed here)
    runname = sys.argv[1]
    startyear = sys.argv[2]
    endyear = sys.argv[3]

    # Extract optional compression argument
    if len(sys.argv) > 4:
        if sys.argv[4].lower() == "compress":
            compress_requested = True
        else:
            print(
                "Too many command line aguments passed OR compression argument not understandable"
            )
            print("If you would like compression, enter 'compress' as the 5th argument")
            print("Exiting...")
            sys.exit(0)
    # Otherwise do not compress
    else:
        compress_requested = False
        print("No compression argument passed -> data will not be compressed")

    # Set variable for 6hrL master
    master_6hrL = "master_cmor3_6hrL.ksh"

    # Convert startyear and endyear to integers
    try:
        startyear = int(startyear)
        endyear = int(endyear)
    except ValueError:
        print("Error: startyear and endyear must be integers")
        sys.exit(1)

    # Export path
    set_path()

    # Print vars running
    print("\n----------------- CMOR EXECUTION DETAILS -----------------")
    print(f"| Master:   {master}")
    print(f"| Runname:  {runname}")
    print(f"| Startyear: {startyear}")
    print(f"| Endyear:   {endyear}")
    print("--------------------------------------------------------\n")

    # 3hr
    process_cmor_data_chunk(master, runname, startyear, endyear, "3hr", 8, 5, "n")
    # 6hr2d
    process_cmor_data_chunk(master, runname, startyear, endyear, "6hr2d", 4, 25, "n")
    # 6hrP
    process_cmor_data_chunk(master, runname, startyear, endyear, "6hrP", 4, 1, "n")
    # day2d
    process_cmor_data_chunk(master, runname, startyear, endyear, "day2d", 1, 50, "n")
    # day3d
    process_cmor_data_chunk(master, runname, startyear, endyear, "day3d", 1, 5, "n")
    # 6hrL
    process_cmor_data_chunk(master_6hrL, runname, startyear, endyear, "6hrL", 4, 1, "y")

    # Compress the data if argument passed
    compress_all(compress_requested)

    # Send automatic email
    details = f"Subdaily CMOR process for run: {runname} from {startyear} to {endyear}"
    script_type = "Subdaily CMOR processing"
    start_time_str = str(start_time)
    email_command = [
        "python",
        "/discover/nobackup/aherron1/automation/send_email.py",
        start_time_str,
        details,
        script_type,
    ]
    subprocess.run(email_command)


# Run it
run()

print("------ Subdaily CMORization Completed Successfully ------")
