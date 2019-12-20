# -*- coding: utf-8 -*-
"""Fixtures for tests.
"""

import os
import shutil

import pytest

from . import TEMP_PATH


# %% Session

@pytest.fixture(scope='session')
def clear_temp_files():
    """Clear all the temporary files generated during tests.
    """

    shutil.rmtree(TEMP_PATH)

    try:
        os.mkdir(TEMP_PATH)
    except FileExistsError:
        pass


# %% reader objects

#@pytest.fixture
#def r():

#    return BaseReader(constants.DATA_FILES[0]['file'])


#@pytest.fixture(params=constants.DATA_FILES, ids=constants.DATA_FILE_IDS)
#def r_all(request):

#    kwargs = constants.get_basereader_args(request.param)

#    return BaseReader(**kwargs)


# %% gazedata objects

#@pytest.fixture
#def gd():

#    return GazeData(constants.ARRAY, **constants.ATTRIBUTES)


#params = constants.VALID_INIT_TYPES.values()
#ids = list(constants.VALID_INIT_TYPES.keys())
#@pytest.fixture(params=params, ids=ids)
#def gd_all(request):

#    return GazeData(request.param, **constants.ATTRIBUTES)


#@pytest.fixture
#def sacc():

#    return Saccade(constants.SACCADE, **constants.ATTRIBUTES)
