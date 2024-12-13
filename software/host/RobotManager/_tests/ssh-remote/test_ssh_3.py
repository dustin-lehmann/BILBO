import os
import paramiko
import subprocess

from utils.network.network import resolve_hostname


def is_host_reachable(hostname):
    """Check if the hostname is reachable (Windows version)."""
    response = subprocess.run(['ping', '-n', '1', hostname], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return response.returncode == 0


def execute_remote_command(hostname, username, password, command):
    """Execute a command on a remote server via SSH."""
    try:
        # Initialize SSH client
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the host
        print(f"Connecting to {hostname}...")
        client.connect(hostname, username=username, password=password)
        print("Connection successful!")

        # Execute the command
        stdin, stdout, stderr = client.exec_command(command)
        print("Command executed. Output:")
        print(stdout.read().decode('utf-8'))
        print("Errors (if any):")
        print(stderr.read().decode('utf-8'))

        # Close the connection
        client.close()
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":

    ip = resolve_hostname('twipr5')
    # Configuration
    hostname = ip  # Replace with the hostname or IP
    username = "lehmann"
    password = "scioip11"
    start_command = "python3 ./software/main.py"
    stop_command = "pkill -f 'python3 ./software/main.py'"  # Use pkill to terminate the program

    # Check if the host is reachable
    if is_host_reachable(hostname):
        print(f"{hostname} is reachable.")

        # Prompt user for action
        action = input("Do you want to (1) Start or (2) Stop the program? Enter 1 or 2: ").strip()

        if action == "1":
            print("Starting the program...")
            execute_remote_command(hostname, username, password, start_command)
        elif action == "2":
            print("Stopping the program...")
            execute_remote_command(hostname, username, password, stop_command)
        else:
            print("Invalid option. Exiting.")
    else:
        print(f"{hostname} is not reachable. Check your network connection or hostname.")
