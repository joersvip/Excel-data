#!/bin/bash
# Script to compile and package Excel Data Center into a standalone Linux binary

set -e

echo "=========================================="
echo "   Excel Data Center - Linux Packager   "
echo "=========================================="

# Ensure .venv is set up
if [ ! -d ".venv" ]; then
    echo "Setting up temporary virtual environment..."
    python3 -m venv .venv
fi

source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Ensure pyinstaller is installed
if ! pip show pyinstaller &> /dev/null; then
    echo "Installing PyInstaller..."
    pip install pyinstaller
fi

# Ensure assets are generated
echo "Generating assets..."
python3 create_assets.py

echo "Compiling application with PyInstaller/Flet..."
# We compile main.py, adding the assets and data folder so that the built application runs with all its files.
flet pack main.py --add-data "assets:assets" --add-data "data:data" --name "excel-data-center"

echo ""
echo "=========================================="
echo "Kompilasi Berhasil!"
echo "File executable Linux Anda berada di folder 'dist/'"
echo "=========================================="
