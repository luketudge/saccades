# -*- coding: utf-8 -*-

import glob
import os

import pytest

from . import constants

from saccades import gazedata


@pytest.fixture(scope='session')
def clear_image_files():

    image_files = glob.glob(os.path.join(constants.IMAGES_PATH, 'test_*'))

    for file in image_files:
        try:
            os.remove(file)
        except FileNotFoundError:
            pass


@pytest.fixture
def gd():

    return gazedata.GazeData(constants.ARRAY)


@pytest.fixture(params=constants.VALID_INIT_TYPES, ids=constants.VALID_INIT_TYPE_NAMES)
def gd_all(request):

    return gazedata.GazeData(request.param)
