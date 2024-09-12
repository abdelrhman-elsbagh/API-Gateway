#!/bin/bash

# Log file location
LOG_FILE="/home/ubuntu/exec_time.log"

# Function to record execution time
record_execution_time() {
    echo "Execution time: $(date)" >> "$LOG_FILE"
}

# Record execution time
record_execution_time

# Kill any running instance of t3.py
pkill -f t3.py
#echo "Executed pkill -f t3.py" >> "$LOG_FILE"

# Log current processes
#ps -ef | grep t3.py >> "$LOG_FILE"
ps -ef | grep t3.py
#echo "Logged processes after pkill" >> "$LOG_FILE"

# Activate virtual environment, update repository, and run t3.py
source /home/ubuntu/myenv/bin/activate
#echo "Activated virtual environment" >> "$LOG_FILE"

cd /home/ubuntu/API-Gateway/
git stash
git pull
cd indv/
echo "Updated git repository" >> "$LOG_FILE"

# Run t3.py if not already running
if ! pgrep -f t3.py > /dev/null; then
    echo "Starting t3.py" >> "$LOG_FILE"
    nohup python3 t3.py
else
    echo "t3.py is already running" >> "$LOG_FILE"
fi