# -*- coding: utf-8 -*-
"""Fixtures for tests.
"""

import os
import shutil

import pytest

from . import TEMP_PATH
from .cases import reading


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
def file(request):

    return request.param
