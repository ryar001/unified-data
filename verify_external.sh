#!/bin/bash
set -e

# 1. Clean previous runs
TEMP_DIR="/tmp/unified_data_verify"
echo "--- Setting up simulation in $TEMP_DIR ---"
rm -rf "$TEMP_DIR"
mkdir -p "$TEMP_DIR"

# 2. Build the package
echo "--- Building package ---"
python3 -m build

# 3. Create a fresh virtual environment
echo "--- Creating fresh virtual environment ---"
python3 -m venv "$TEMP_DIR/venv"
source "$TEMP_DIR/venv/bin/activate"

# 4. Install the build package and its dependencies
echo "--- Installing package into venv ---"
# Find the latest wheel
WHEEL=$(ls -t dist/*.whl | head -n 1)
pip install "$WHEEL"

# 5. Copy the verification test to the isolated directory
cp tests/test_verify_install.py "$TEMP_DIR/"

# 6. Run the test from the isolated directory
echo "--- Running verification test from isolated directory ---"
cd "$TEMP_DIR"
python3 test_verify_install.py

echo "--- SIMULATION SUCCESSFUL ---"
echo "The package 'unified-data' is correctly installable and usable as an external dependency."
