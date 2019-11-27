#!/bin/bash -v

# Run this from the project root directory,
# where install.sh is located.

# Check code style.
flake8 saccades tests

# Install.
./install.sh

# Run the tests and coverage report.
pytest -v --cov=saccades --cov-report=term-missing

# Build the documentation.
make -C docs html
