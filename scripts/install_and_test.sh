#!/bin/bash

# Run this from the project root directory.

echo
echo '#### Install ####'
echo
./scripts/install.sh

echo
echo '#### Tests ####'
echo
pytest -v --cov=saccades --cov-report=term-missing

echo
echo '#### Code style checks ####'
echo
./scripts/check_style.sh

echo
echo '#### Docs ####'
echo
./scripts/build_docs.sh
