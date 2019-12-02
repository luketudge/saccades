# -*- coding: utf-8 -*-

import pytest

from . import constants

from saccades import gazedata


@pytest.fixture
def gd():
    return gazedata.GazeData(constants.ARRAY)
