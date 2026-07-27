#!/bin/bash
# Install Excel Data Center into Linux Desktop Applications Menu

set -e

echo "=========================================="
echo "   Excel Data Center - Desktop Installer  "
echo "=========================================="

# Get the absolute path of this directory
APP_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

echo "Directory aplikasi: $APP_DIR"

# Template .desktop file
TEMPLATE_FILE="$APP_DIR/excel-data-center.desktop"
TEMP_FILE="/tmp/excel-data-center.desktop"

if [ ! -f "$TEMPLATE_FILE" ]; then
    echo "Error: excel-data-center.desktop tidak ditemukan di $APP_DIR!"
    exit 1
fi

# Replace APP_DIR with the real absolute path
sed "s|APP_DIR|$APP_DIR|g" "$TEMPLATE_FILE" > "$TEMP_FILE"

# Make run_linux.sh executable
chmod +x "$APP_DIR/run_linux.sh"

# Install to users local application directory
TARGET_DIR="$HOME/.local/share/applications"
mkdir -p "$TARGET_DIR"

cp "$TEMP_FILE" "$TARGET_DIR/excel-data-center.desktop"
chmod +x "$TARGET_DIR/excel-data-center.desktop"

echo "Shortcut desktop berhasil diinstal ke $TARGET_DIR"
echo "Aplikasi sekarang dapat diluncurkan langsung dari Menu Aplikasi (Application Launcher) Anda!"
