import subprocess
import time
import sys
from datetime import datetime


def send_email(start_time, command_array_str, script_type):
    # Split the command array using the delimiter
    command_array = command_array_str.split(";")

    # Email configuration
    recipient = "alexander.herron@nasa.gov"
    subject = f"Script Completion Alert - {script_type}"
    body = f"Dear Noble Scientific Programmer,\n\n"

    # Record start/end time
    start_time_readable = datetime.utcfromtimestamp(start_time).strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    end_time = time.time()
    end_time_readable = datetime.utcfromtimestamp(end_time).strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    # Calculate duration
    duration = end_time - start_time
    days, remainder = divmod(duration, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    duration_readable = f"{int(days)} days, {int(hours)} hours, {int(minutes)} minutes, {int(seconds)} seconds"

    # Add timing content to body
    body += f"Your {script_type} script has been completed.\n\nStart time: {start_time_readable}\n"
    body += f"End time: {end_time_readable}\n"
    body += f"Duration: {duration_readable}\n\n"

    # Add commands (if command array is not empty)
    if command_array:
        body += "Commands:\n\n"
        body += "\n".join(command_array) + "\n\n"

    # Email footer
    body += "Sincerely,\nYour humble email.sh script"

    # Command to send email using mailx
    mailx_command = f'echo -e "{body}" | mailx -s "{subject}" {recipient}'

    # Execute the command using subprocess
    try:
        subprocess.run(mailx_command, shell=True, check=True, text=True)
        print("Email sent successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error sending email: {e}")
    finally:
        # Print execution time
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time: {execution_time} seconds")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(
            "Usage: python send_email.py <start_time> '<command_array>' <script_type>"
        )
        sys.exit(1)

    start_time = float(sys.argv[1])
    command_array_str = sys.argv[2]
    script_type = sys.argv[3]

    send_email(start_time, command_array_str, script_type)
