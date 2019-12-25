# -*- coding: utf-8 -*-
"""Test the Saccade class.

Saccade attributes that call functions from the metrics module
are tested in the tests for that module.
"""

import pandas

from . import helpers

from saccades import GazeData
from saccades import Saccade


# %% __init__()

def test_init_from_GazeData(gaze_data):

    gd = helpers.init_gazedata(gaze_data)
    sacc = Saccade(gd)

    assert isinstance(sacc, Saccade)
    assert isinstance(sacc, GazeData)
    assert isinstance(sacc, pandas.DataFrame)
