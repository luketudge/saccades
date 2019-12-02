# saccades

[![Build Status](https://www.travis-ci.org/luketudge/saccades.svg?branch=master)](https://www.travis-ci.org/luketudge/saccades)
[![codecov](https://codecov.io/gh/luketudge/saccades/branch/master/graph/badge.svg)](https://codecov.io/gh/luketudge/saccades)

A Python package for working with saccades. A work in progress.

## Aims

Implement algorithms for:

* extracting saccades from eye gaze coordinates
* calculating basic parameters for a saccade, e.g.:
  * latency
  * duration
  * amplitude
  * peak velocity
* calculating the various measures of saccade trajectory deviation described in [this article](https://doi.org/10.3758/s13428-016-0846-6)

## Install

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
