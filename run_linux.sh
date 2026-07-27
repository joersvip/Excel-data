#!/bin/bash
# Script to run Excel Data Center on full Linux systems using Python Virtual Environment

# Exit on error
set -e

echo "=========================================="
echo "   Excel Data Center - Linux Runner   "
echo "=========================================="

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is not installed. Please install Python 3 and try again."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment (.venv)..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

# Generate assets
echo "Generating visual assets..."
python3 create_assets.py

# Launch Flet app
echo "Launching Excel Data Center..."
# In a local Linux environment with a graphic interface, this opens Flet as a native app.
# If headless, Flet automatically serves via web browser fallback.
python3 main.py
