# -*- coding: utf-8 -*-
"""Setup for tests.

Gather test cases from the cases submodule,
and parametrize them into fixtures.
"""

import os
import shutil

import pytest

from . import TEMP_PATH
from .cases import cases_gazedata
from .cases import cases_readers


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

@pytest.fixture(scope='session', autouse=True)
def clear_temp_files():
    """Clear the temporary file directory.
    """

    try:
        shutil.rmtree(TEMP_PATH)
    except FileNotFoundError:
        pass

    try:
        os.makedirs(TEMP_PATH)
    except FileExistsError:
        pass


# %% Data files

@pytest.fixture(**prepare_case(cases_readers.DATA_FILES))
def data_file(request):

    return request.param


@pytest.fixture(**prepare_case(cases_readers.ROW_FORMATS))
def row_format(request):

    return request.param


@pytest.fixture(**prepare_case(cases_readers.DATA_BLOCKS))
def data_block(request):

    return request.param


# %% Gaze data

@pytest.fixture
def gaze_data_1():

    return cases_gazedata.GAZE_DATA['array']


@pytest.fixture(**prepare_case(cases_gazedata.GAZE_DATA))
def gaze_data(request):

    return request.param


@pytest.fixture(**prepare_case(cases_gazedata.INVALID_GAZE_DATA))
def invalid_gaze_data(request):

    return request.param


@pytest.fixture(**prepare_case(cases_gazedata.INDEX))
def index(request):

    return request.param


@pytest.fixture(**prepare_case(cases_gazedata.ATTRIBUTES))
def attributes(request):

    return request.param


@pytest.fixture(**prepare_case(cases_gazedata.METHODS))
def method(request):

    return request.param


@pytest.fixture(**prepare_case(cases_gazedata.DETECTION))
def detection(request):

    return request.param


@pytest.fixture(**prepare_case(cases_gazedata.PLOT))
def plot(request):

    return request.param
