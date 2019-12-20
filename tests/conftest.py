# -*- coding: utf-8 -*-
"""Fixtures for tests.
"""

import os
import shutil

import pytest

from . import TEMP_PATH
from . import helpers
from .cases import reading


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

@pytest.fixture(**helpers.prepare_case(reading.DATA_FILES))
def file(request):

    return request.param
