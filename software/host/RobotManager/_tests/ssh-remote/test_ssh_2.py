import atexit
import os
import paramiko
import subprocess
import threading
import time

from utils.network.network import resolve_hostname

# Global dictionary to track active robots and their retry counts
active_robots = {}
robot_hostnames = [f"twipr{i}" for i in range(1, 11)]

# Constants
PING_RETRIES = 2  # Reduce retries to speed up detection
PING_RETRY_DELAY = 2  # Shorter delay between retries (in seconds)
MONITOR_INTERVAL = 3  # Shorter interval for monitoring loop (in seconds)


def is_host_reachable(hostname):
    """Check if the hostname is reachable."""
    response = subprocess.run(['ping', '-n', '1', hostname], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return response.returncode == 0


# def resolve_hostname(hostname):
#     """Resolve a hostname to an IP address."""
#     try:
#         ip = subprocess.check_output(['ping', '-n', '1', hostname], stderr=subprocess.DEVNULL).decode('utf-8')
#         return ip.split()[2].strip('[]')  # Extract the IP address
#     except Exception:
#         return None


def execute_remote_command(hostname, username, password, command):
    """Execute a command on a remote server via SSH."""
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname, username=username, password=password)
        stdin, stdout, stderr = client.exec_command(command)
        stdout.channel.recv_exit_status()  # Wait for command to complete
        output = stdout.read().decode('utf-8')
        errors = stderr.read().decode('utf-8')
        client.close()
        return output, errors
    except Exception as e:
        print(f"Error executing command on {hostname}: {e}")
        return None, str(e)


def start_robot(hostname, username, password, command):
    """Start the Python program on a robot."""
    print(f"Starting program on {hostname}...")
    output, errors = execute_remote_command(hostname, username, password, command)
    if errors:
        print(f"Error starting program on {hostname}: {errors}")
    else:
        print(f"Program started on {hostname}: {output}")


def stop_robot(hostname, username, password, command):
    """Stop the Python program on a robot."""
    print(f"Stopping program on {hostname}...")
    output, errors = execute_remote_command(hostname, username, password, command)
    if errors:
        print(f"Error stopping program on {hostname}: {errors}")
    else:
        print(f"Program stopped on {hostname}: {output}")


def monitor_robots(username, password, start_command):
    """Continuously monitor robots, handle new and unreachable ones."""
    global active_robots

    while True:
        for robot in robot_hostnames:
            if robot not in active_robots:
                # Check for new robots
                if is_host_reachable(robot):
                    ip = resolve_hostname(robot)
                    print(f"{robot} is reachable on {ip}")
                    if ip:
                        active_robots[robot] = {"ip": ip, "unreachable_retries": 0}
                        start_robot(ip, username, password, start_command)
            else:
                # Monitor active robots for connectivity
                retries = active_robots[robot]["unreachable_retries"]
                if not is_host_reachable(robot):
                    if retries < PING_RETRIES:
                        active_robots[robot]["unreachable_retries"] += 1
                        print(f"{robot} is unreachable. Retry {retries + 1}/{PING_RETRIES}...")
                        time.sleep(PING_RETRY_DELAY)  # Wait before next retry
                    else:
                        print(f"{robot} is no longer reachable. Removing from active list.")
                        del active_robots[robot]  # Remove from active robots
                else:
                    # Reset retry count if the robot is reachable again
                    active_robots[robot]["unreachable_retries"] = 0
        time.sleep(MONITOR_INTERVAL)  # Check more frequently


def startAllRobots():
    """Start the program on all reachable robots and begin monitoring."""
    username = "lehmann"
    password = "scioip11"
    start_command = "python3 ./software/main.py"

    # Start the monitoring thread
    monitor_thread = threading.Thread(target=monitor_robots, args=(username, password, start_command), daemon=True)
    monitor_thread.start()
    print("Monitoring thread started to detect new robots and track active ones.")


def stopAllRobots():
    """Stop the program on all active robots."""
    username = "lehmann"
    password = "scioip11"
    stop_command = "pkill -f 'python3 ./software/main.py'"

    for robot, data in list(active_robots.items()):  # Use list() to avoid runtime modification issues
        ip = data["ip"]
        stop_robot(ip, username, password, stop_command)
    active_robots.clear()
    print("All robots stopped.")


def cleanup():
    """Ensure all robots are stopped when the program exits."""
    print("Cleaning up: stopping all robots...")
    stopAllRobots()


if __name__ == "__main__":
    # Register the cleanup function to run at exit
    atexit.register(cleanup)

    try:
        print("Starting all robots...")
        startAllRobots()
        input("Press Enter to exit and stop all robots...\n")  # Keeps the program running
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received. Exiting...")
    finally:
        cleanup()  # Ensures cleanup even in case of exceptions
