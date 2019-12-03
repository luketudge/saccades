# -*- coding: utf-8 -*-

import pytest

from . import constants

from saccades import gazedata


@pytest.fixture(params=constants.VALID_INIT_TYPES, ids=constants.VALID_INIT_TYPE_NAMES)
def gd(request):
    return gazedata.GazeData(request.param)


@pytest.fixture
def gd_not_parametrized():
    return gazedata.GazeData(constants.ARRAY)
