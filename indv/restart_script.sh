#!/bin/bash

while true; do
    # Kill any running instance of t3.py
    pkill -f t3.py

    echo "Starting t3.py at $(date)"
    python3 t3.py &  # Run t3.py in the background

    echo "t3.py started. Waiting for 12 hours before restarting..."
    sleep 12h  # Wait for 12 hours
done
