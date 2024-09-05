#!/bin/bash

while true; do
    # Kill any running instance of t3.py
    pkill -f t3.py

    echo "Starting t3.py at $(date)"
    nohup python3 t3.py > t3_output.log 2>&1 &  # Run t3.py independently using nohup

    echo "t3.py started. Waiting for 20 hours before restarting..."
    sleep 20h  # Wait for 20 hours

    # After 20 hours, delete the log file
    echo "Deleting log file..."
    rm -f restart_script.log

    # Relaunch restart_script.sh and exit the current instance
    echo "Restarting restart_script.sh"
    nohup ./restart_script.sh > restart_script.log 2>&1 &  # Relaunch itself
    exit 0  # Exit the current instance
done
