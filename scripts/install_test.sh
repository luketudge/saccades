#!/bin/bash -v

# Run this from the project root directory.

./scripts/install.sh
pytest -v --cov=saccades --cov-report=term-missing

./scripts/install.sh
./scripts/build_docs.sh
