#!/usr/bin/env python3

import subprocess
import time
import os
import signal
import shutil

def run_ros_command(command):
    """Run a ROS command using subprocess."""
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running command '{command}': {e}")

def delete_existing_directories():
    """Delete existing directories if they exist."""
    directories = ['data1', 'data2', 'position1', 'position2']
    for directory in directories:
        if os.path.exists(directory):
            print(f"Deleting existing directory: {directory}")
            shutil.rmtree(directory)  # Remove the directory and all its contents
        else:
            print(f"No existing directory found: {directory}")

def main():
    # Change to the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)  # Change to the script's directory

    # Delete existing directories
    delete_existing_directories()

    # Commands to run the dvl_a50 node with different IP addresses
    command1 = "ros2 run dvl_a50 dvl_a50.py --ros-args -p ip_address:='192.168.0.80'"
    command2 = "ros2 run dvl_a50 dvl_a50.py --ros-args -p ip_address:='192.168.0.81'"

    # Start the first command in a separate process group
    proc1 = subprocess.Popen(command1, shell=True, preexec_fn=os.setsid)
    time.sleep(1)  # Allow some time for the first process to initialize

    # Start the second command in a separate process group
    proc2 = subprocess.Popen(command2, shell=True, preexec_fn=os.setsid)
    time.sleep(2)  # Allow time for both processes to start

    # Define commands to record the topics into rosbag
    rosbag_commands = [
        "ros2 bag record -o data1 /dvl/data1",
        "ros2 bag record -o data2 /dvl/data2",
        "ros2 bag record -o position1 /dvl/position1",
        "ros2 bag record -o position2 /dvl/position2"
    ]

    # Start recording rosbag data
    for command in rosbag_commands:
        subprocess.Popen(command, shell=True)

    print("ROS nodes are running and topics are being recorded.")

    # Wait for the processes to complete (you may want to replace with appropriate exit handling)
    try:
        proc1.wait()
        proc2.wait()
    except KeyboardInterrupt:
        print("Stopping the ROS nodes...")
        os.killpg(os.getpgid(proc1.pid), signal.SIGTERM)  # Terminate process group
        os.killpg(os.getpgid(proc2.pid), signal.SIGTERM)  # Terminate process group
        print("Nodes terminated.")

if __name__ == '__main__':
    main()
