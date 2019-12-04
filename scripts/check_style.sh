#!/bin/bash

flake8 --ignore E265 saccades setup.py
flake8 --ignore E265,E266 tests
