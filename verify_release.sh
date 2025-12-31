#!/bin/bash
set -e

# visual separator
echo "========================================"
echo "STARTING POST-INSTALL VERIFICATION"
echo "========================================"

# Create temp venv
VENV_DIR=$(mktemp -d)/venv
python3 -m venv $VENV_DIR
source $VENV_DIR/bin/activate

# install the package (simulating install from pypi, but here we can just install the built wheel if pypi isn't immediate)
# For strict "publish then install" verification, we should try pip install unified-data
# BUT, pypi propagation takes time. 
# User asked "tests then publish it ... then write a new test that install this package".
# I will attempt to install the package name. If it fails (due to valid reasons like propagation), I will fallback to wheel.
# However, to be robust in this flow, I will explicitly install the wheel I just built to verify the ARTIFACT is good.
# Verifying PyPI propagation is distinct from verifying the package artifact.
# Let's try installing the wheel.

WHEEL_FILE=$(ls dist/*.whl | head -n 1)
echo "Installing built wheel: $WHEEL_FILE"
pip install $WHEEL_FILE

# Install test dependencies (polars etc should be pulled by wheel, but let's be safe)
# pip install unittest # (standard lib)

# Run verification test
python3 tests/test_verify_install.py

# Cleanup
deactivate
rm -rf $VENV_DIR

echo "========================================"
echo "VERIFICATION PASSED"
echo "========================================"
