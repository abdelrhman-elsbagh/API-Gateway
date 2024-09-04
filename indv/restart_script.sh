#!/bin/bash

while true; do
    # Kill any running instance of t3.py
    pkill -f restart_script.sh
    pkill -f t3.py

    echo "Starting t3.py at $(date)"
    python3 t3.py &  # Run t3.py in the background

    echo "t3.py started. Waiting for 12 hours before restarting..."
    sleep 12h  # Wait for 12 hours

    # After 12 hours, delete the log file
    echo "Deleting log file..."
    rm -f restart_script.log
done
