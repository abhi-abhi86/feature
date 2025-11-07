#!/bin/bash

# This script is a placeholder for building a distributable installer for the application.
# It uses PyInstaller as an example, which packages a Python application and all its
# dependencies into a single executable.

# --- Prerequisites ---
# 1. Install PyInstaller: pip install pyinstaller
# 2. Ensure the application runs correctly using `run_app.sh`.

echo "--- Trading Agent AI Installer Builder ---"

# Get the directory of the script
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)
PROJECT_ROOT="$SCRIPT_DIR/.."

MAIN_APP_PY="$PROJECT_ROOT/src/main_app.py"
APP_NAME="TradingAgentAI"

# Check if the main script exists
if [ ! -f "$MAIN_APP_PY" ]; then
    echo "Error: Main application script not found at $MAIN_APP_PY" >&2
    exit 1
fi

# Activate virtual environment if it exists
if [ -d "$PROJECT_ROOT/venv" ]; then
    echo "Activating Python virtual environment..."
    source "$PROJECT_ROOT/venv/bin/activate"
fi

echo "Starting PyInstaller build..."

# PyInstaller command
# --name: The name of the executable and the build folder.
# --onefile: Create a one-file bundled executable.
# --windowed: Prevents a console window from being displayed when the GUI is running.
# --add-data: To bundle non-code files like configs, models, or UI assets.
#   The format is 'SOURCE:DESTINATION'. On Windows, use ';' as the separator, on macOS/Linux use ':'.

# Determine the separator for --add-data based on the OS
SEPARATOR=":"
if [[ "$OSTYPE" == "cygwin" || "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    SEPARATOR=";"
fi

pyinstaller \
    --name "$APP_NAME" \
    --onefile \
    --windowed \
    --add-data "${PROJECT_ROOT}/config/main_config.ini${SEPARATOR}config" \
    --add-data "${PROJECT_ROOT}/config/logging.ini${SEPARATOR}config" \
    --add-data "${PROJECT_ROOT}/models/vision/best.pt${SEPARATOR}models/vision" \
    --add-data "${PROJECT_ROOT}/models/prediction/lstm_transformer.pt${SEPARATOR}models/prediction" \
    --hidden-import "pyqtgraph.graphicsItems.ViewBox.axisCtrlTemplate_pyqt5_vb"
    --hidden-import "pyqtgraph.graphicsItems.PlotItem.plotConfigTemplate_pyqt5"
    --clean \
    "$MAIN_APP_PY"

BUILD_EXIT_CODE=$?

if [ $BUILD_EXIT_CODE -eq 0 ]; then
    echo "Build successful!"
    echo "The executable can be found in the '$PROJECT_ROOT/dist' directory."
else
    echo "Build failed. See the output above for details." >&2
    exit 1
fi

# Deactivate virtual environment
if [ -d "$PROJECT_ROOT/venv" ]; then
    deactivate
fi

echo "-----------------------------------------"
