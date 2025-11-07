#!/bin/bash

# This script runs the entire test suite for the application using pytest.

echo "--- Running Trading Agent AI Test Suite ---"

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

# Check if pytest is installed
if ! command -v pytest &> /dev/null
then
    echo "pytest could not be found. Please install it with: pip install pytest" >&2
    exit 1
fi

# Set the Python path to include the project root
export PYTHONPATH="$PROJECT_ROOT:$PYTHONPATH"

# The directory containing the tests
TESTS_DIR="$PROJECT_ROOT/tests"

if [ ! -d "$TESTS_DIR" ]; then
    echo "Error: Tests directory not found at $TESTS_DIR" >&2
    exit 1
fi

echo "Discovering and running tests with pytest..."

# Run pytest
# -v: for verbose output
pytest -v "$TESTS_DIR"

TEST_EXIT_CODE=$?

# Deactivate virtual environment
if [ -d "$PROJECT_ROOT/venv" ]; then
    deactivate
fi

if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo "All tests passed successfully!"
else
    echo "One or more tests failed. See the output above for details." >&2
    exit 1
fi

echo "-----------------------------------------"
