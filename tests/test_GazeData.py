# -*- coding: utf-8 -*-
"""Test the GazeData class.
"""

import numpy

from saccades import GazeData


# %% Helper functions

def init_gazedata(data):
    """Initialize a GazeData table from a gaze data test case.
    """

    return GazeData(data['in']['data'])


# %% __init__()

def test_init(gaze_data):
    """Test initializing a GazeData table.
    """

    gd = init_gazedata(gaze_data)

    assert isinstance(gd, GazeData)
    assert numpy.array_equal(gd[['time', 'x', 'y']], gaze_data['out']['data'])
