# -*- coding: utf-8 -*-

import numpy
import pandas

from . import constants

from saccades import gazedata


# GazeData methods that wrap functions from other modules
# are tested in the test files for those modules.
# This test file tests the other features of the GazeData class.


#%% __init__()

def test_GazeData_init_types():

    for input_type in [constants.SEQUENCE, constants.ARRAY, constants.DATAFRAME]:
        gd = gazedata.GazeData(input_type)
        assert isinstance(gd, gazedata.GazeData)
        assert isinstance(gd, pandas.DataFrame)
        assert numpy.array_equal(gd, constants.ARRAY)
        assert list(gd.columns) == ['time', 'x', 'y']


# Check we get a copy and not a view.
def test_GazeData_is_not_view():

    gd = gazedata.GazeData(constants.ARRAY)
    gd['time'][0] = 9000.

    assert constants.ARRAY[0, 0] != 9000.


#%% Subsetting

# Subsetting instances of the GazeData class presents some technical problems.
# We would like different subsetting operations to return different types.
# A subset of rows is still a valid table of gaze data.
# So this should return an instance of the GazeData class.
# A subset of columns is coordinates or some other incomplete view of the data.
# So this should not return an instance of the GazeData class.
# But a subset of composed of the 'time', 'x', and 'y' columns *is* complete.
# So this column subset should return an instance of the GazeData class.

def test_subset_rows():

    gd = gazedata.GazeData(constants.ARRAY)
    gd_subset = gd[:2]
    assert numpy.array_equal(gd_subset, constants.ARRAY[:2, :])
    assert isinstance(gd_subset, gazedata.GazeData)


def test_subset_incomplete_cols():

    gd = gazedata.GazeData(constants.ARRAY)
    gd_subset = gd[['x', 'y']]
    assert numpy.array_equal(gd_subset, constants.ARRAY_XY)
    assert not isinstance(gd_subset, gazedata.GazeData)


def test_subset_complete_cols():

    gd = gazedata.GazeData(constants.ARRAY)
    gd_subset = gd[['time', 'x', 'y']]
    assert numpy.array_equal(gd_subset, constants.ARRAY)
    assert isinstance(gd_subset, gazedata.GazeData)
