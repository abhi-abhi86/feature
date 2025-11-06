#!/bin/bash

# This script is the main entry point for running the AI-Powered Trading Agent.

# Get the directory of the script
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)
PROJECT_ROOT="$SCRIPT_DIR/.."

# Activate virtual environment if it exists
if [ -d "$PROJECT_ROOT/venv" ]; then
    echo "Activating Python virtual environment..."
    source "$PROJECT_ROOT/venv/bin/activate"
else
    echo "Virtual environment not found. Running with system Python."
fi

# Set the Python path to include the project root
export PYTHONPATH="$PROJECT_ROOT:$PYTHONPATH"

# Run the main application
MAIN_APP_PATH="$PROJECT_ROOT/src/main_app.py"

if [ -f "$MAIN_APP_PATH" ]; then
    echo "Starting the Trading Agent AI..."
    python "$MAIN_APP_PATH"
else
    echo "Error: Main application file not found at $MAIN_APP_PATH"
    exit 1
fi

# Deactivate virtual environment on exit
if [ -d "$PROJECT_ROOT/venv" ]; then
    deactivate
fi

echo "Application has been shut down."
