# -*- coding: utf-8 -*-

import glob
import os

import pytest

from . import constants

from saccades import GazeData
from saccades import Saccade
from saccades.readers import BaseReader


# %% Test session setup

@pytest.fixture(scope='session')
def clear_image_files():

    image_files = glob.glob(os.path.join(constants.IMAGES_PATH, 'test_*'))

    for file in image_files:
        try:
            os.remove(file)
        except FileNotFoundError:
            pass


# %% readers

@pytest.fixture
def r():

    return BaseReader(constants.DATA_FILES[0]['file'])


ids = [x['filename'] for x in constants.DATA_FILES]
@pytest.fixture(params=constants.DATA_FILES, ids=ids)
def r_all(request):

    kwargs = {'file': request.param['file']}

    if 'sep' in request.param:
        kwargs['sep'] = request.param['sep']

    return BaseReader(**kwargs)


# %% gazedata objects

@pytest.fixture
def gd():

    return GazeData(constants.ARRAY, **constants.ATTRIBUTES)


params = constants.VALID_INIT_TYPES.values()
ids = list(constants.VALID_INIT_TYPES.keys())
@pytest.fixture(params=params, ids=ids)
def gd_all(request):

    return GazeData(request.param, **constants.ATTRIBUTES)


@pytest.fixture
def sacc():

    return Saccade(constants.SACCADE, **constants.ATTRIBUTES)
