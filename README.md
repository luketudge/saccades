# saccades

[![Build Status](https://www.travis-ci.org/luketudge/saccades.svg?branch=master)](https://www.travis-ci.org/luketudge/saccades)
[![codecov](https://codecov.io/gh/luketudge/saccades/branch/master/graph/badge.svg)](https://codecov.io/gh/luketudge/saccades)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/luketudge/saccades.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/luketudge/saccades/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/luketudge/saccades.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/luketudge/saccades/context:python)

A Python package for working with saccades. A work in progress.

## Status

We currently have:

* Classes for representing eyetracking coordinates and saccades.
* Methods for calculating velocity and acceleration.
* Conversion from screen pixels to degrees of visual angle.
* Methods for saccade detection.
* Methods for calculating some saccade parameters.

## TODO

Some things still to be implemented, in approximate order of priority:

* A sequence-like class that groups blocks of eyetracking coordinates as trials in an experiment.
* Functions for reading various text eyetracking data files.
* A quick-start page for the documentation, and some example notebooks.
* Methods for gaze coordinate smoothing.
* More saccade detection algorithms.
* More saccade parameters.

## Install

How to install and test the current development version.

### Virtual environment

Create and activate a virtual environment, for example using *virtualenv* as described in the [Hitchhiker's Guide to Python](https://docs.python-guide.org/dev/virtualenvs/#lower-level-virtualenv):

```shell
virtualenv -p /usr/bin/python3 .venv
source .venv/bin/activate
```

You may need to replace `/usr/bin/python3` with the path to your Python 3 executable.

### Clone repository

Clone this repository to download the latest source code, then switch into the newly-cloned directory:

```shell
git clone https://github.com/luketudge/saccades.git
cd saccades
```

### Install

Run the installation and testing script [install_and_test.sh](scripts/install_and_test.sh) to install the package and run the tests (you may need to change the permissions for this file to allow executing it as a program):

```python
./scripts/install_and_test.sh
```

If you make changes to the source code (in the main package directory [saccades](saccades)), you can run this script again to build and test your modified version.

## Example

You can see an example script (of sorts) in [test_script.py](tests/test_script.py).
