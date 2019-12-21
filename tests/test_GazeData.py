# -*- coding: utf-8 -*-
"""Test the GazeData class.

GazeData methods that wrap functions from other modules
are tested in the test files for those modules.
Compatibility of GazeData objects with other data science packages
is tested in test_compatibility.py.
This test file tests the other features of the GazeData class.
"""

import numpy
import pandas
import pytest

from saccades import GazeData


# %% Helper functions

def init_gazedata(data):
    """Initialize a GazeData table from a gaze data test case.
    """

    return GazeData(data['in']['data'])


# %% __init__()

def test_init(gaze_data):
    """Test initializing a GazeData table.

    It should be a subclass of pandas.DataFrame.
    The column names should be intact
    or replaced with time, x, and y if these are not supplied.
    """

    gd = init_gazedata(gaze_data)

    assert isinstance(gd, GazeData)
    assert isinstance(gd, pandas.DataFrame)
    assert set(gd.columns) == set(gaze_data['out']['columns'])
    assert numpy.array_equal(gd[['time', 'x', 'y']], gaze_data['out']['data'])


def test_invalid_init(invalid_gaze_data):
    """Check that invalid data raises the expected exception.
    """

    with pytest.raises(invalid_gaze_data['out']['exception']):
        init_gazedata(invalid_gaze_data)


def test_empty_init():
    """Test initializing a GazeData table without data.

    The columns time, x, and y should be initialized but empty.
    """

    gd = GazeData()

    assert set(gd.columns) == set(['time', 'x', 'y'])
    assert numpy.array_equal(gd, numpy.empty(shape=[0, 3]))


def test_GazeData_is_not_view():
    """Check that a GazeData table is not a view of the init data
    (i.e. that changes won't propagate back to the init data).
    """

    a = numpy.array([[0., 1., 2.],
                     [2., 3., 4.]])
    gd = GazeData(a)
    gd['time'] = 9000.

    assert a[0, 0] != 9000.
