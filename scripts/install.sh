#!/bin/bash

# Check that we are in a virtual environment.
# (Prevents accidentally installing into the root environment).
if test -z "$VIRTUAL_ENV"
then
    echo "No virtual environment detected. Exiting."
    exit 1
fi

# Use requirements.txt for the runtime dependencies.
# Don't pin these.
# Use test_requirements.txt just for the testing environment.
# Make this reproducible by pinning all versions.
pip install -r requirements.txt
pip install -r test_requirements.txt

# Use setup.py for actual package dependencies.
# Don't pin these.
python setup.py bdist_wheel
pip install --force-reinstall dist/saccades*.whl
