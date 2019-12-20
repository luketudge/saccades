# -*- coding: utf-8 -*-
"""Setup for tests.

Gather test cases from the cases submodule,
and parametrize them into fixtures.
"""

import os
import shutil

import pytest

from . import TEMP_PATH
from .cases import reading


# %% Command line options

# https://docs.pytest.org/en/latest/example/simple.html#control-skipping-of-tests-according-to-command-line-option

def pytest_addoption(parser):

    parser.addoption('--quick',
                     action='store_true',
                     default=False,
                     help='exclude slow tests')


def pytest_configure(config):

    config.addinivalue_line('markers', 'slow: mark test as slow to run')


def pytest_collection_modifyitems(config, items):

    if config.getoption('--quick'):
        skip_slow = pytest.mark.skip(reason='not run with --quick option')
        for item in items:
            if 'slow' in item.keywords:
                item.add_marker(skip_slow)


# %% Helper functions

def prepare_case(case):
    """Turn a test case into keyword arguments for pytest.fixture().

    The keys of the case dictionary become the ids argument.
    The values become the params argument.
    """

    return {'params': case.values(), 'ids': list(case.keys())}


# %% Session fixtures

@pytest.fixture(scope='session')
def clear_temp_files():
    """Clear all the temporary files generated during tests.
    """

    shutil.rmtree(TEMP_PATH)

    try:
        os.mkdir(TEMP_PATH)
    except FileExistsError:
        pass


# %% Data files

@pytest.fixture(**prepare_case(reading.DATA_FILES))
def data_file(request):

    return request.param


@pytest.fixture(**prepare_case(reading.ROW_FORMATS))
def row_format(request):

    return request.param


@pytest.fixture(**prepare_case(reading.DATA_BLOCKS))
def data_block(request):

    return request.param
