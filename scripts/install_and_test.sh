#!/bin/bash

# Run this from the project root directory.

echo
echo '#### Install ####'
echo
./scripts/install.sh

echo
echo '#### Tests ####'
echo
./scripts/test.sh

echo
echo '#### Code style checks ####'
echo
./scripts/check_style.sh

echo
echo '#### Docs ####'
echo
./scripts/build_docs.sh
