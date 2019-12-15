# -*- coding: utf-8 -*-

import glob
import os

import pytest

from . import constants

from saccades import GazeData
from saccades import Saccade
from saccades.readers import BaseReader


#%% Test session setup

@pytest.fixture(scope='session')
def clear_image_files():

    image_files = glob.glob(os.path.join(constants.IMAGES_PATH, 'test_*'))

    for file in image_files:
        try:
            os.remove(file)
        except FileNotFoundError:
            pass


#%% readers

@pytest.fixture
def r():

    filepath = os.path.join(constants.DATA_PATH, constants.FILENAMES[0])

    return BaseReader(filepath)


@pytest.fixture(params=constants.FILENAMES)
def r_all(request):

    filepath = os.path.join(constants.DATA_PATH, request.param)

    return BaseReader(filepath)


#%% gazedata objects

@pytest.fixture
def gd():

    return GazeData(constants.ARRAY, **constants.ATTRIBUTES)


@pytest.fixture(params=constants.VALID_INIT_TYPES, ids=constants.VALID_INIT_TYPE_NAMES)
def gd_all(request):

    return GazeData(request.param, **constants.ATTRIBUTES)


@pytest.fixture
def sacc():

    return Saccade(constants.SACCADE, **constants.ATTRIBUTES)
