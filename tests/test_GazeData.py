# -*- coding: utf-8 -*-

import numpy
import pandas
import pytest

from . import constants

from saccades import gazedata


# GazeData methods that wrap functions from other modules
# are tested in the test files for those modules.
# This test file tests the other features of the GazeData class.


#%% __init__()

@pytest.mark.parametrize('input_type', constants.INIT_TYPES)
def test_GazeData_init_types(input_type):

    gd = gazedata.GazeData(input_type)
    assert isinstance(gd, gazedata.GazeData)
    assert isinstance(gd, pandas.DataFrame)
    assert list(gd.columns[:3]) == ['time', 'x', 'y']
    assert numpy.array_equal(gd[['time', 'x', 'y']], constants.ARRAY[:, :3])


def test_empty_GazeData():

    gd = gazedata.GazeData()
    assert isinstance(gd, gazedata.GazeData)
    assert isinstance(gd, pandas.DataFrame)
    assert list(gd.columns) == ['time', 'x', 'y']
    assert gd.empty


# Check we get a copy and not a view.
def test_GazeData_is_not_view():

    a = constants.ARRAY
    gd = gazedata.GazeData(a)
    gd['time'][0] = 9000.

    assert a[0, 0] != 9000.


#%% Subsetting

# Subsetting instances of the GazeData class presents some technical problems.
# We would like different subsetting operations to return different types.
# A subset of rows is still a valid table of gaze data.
# So this should return an instance of the GazeData class.
# Likewise a subset composed of the 'time', 'x', and 'y' columns is complete.
# So this column subset should also return an instance of the GazeData class.
# But a subset of other columns is an incomplete view of the data.
# So this should not return an instance of the GazeData class.

def test_subset_rows(gd):

    gd_subset = gd[:2]
    assert numpy.array_equal(gd_subset, constants.ARRAY[:2, :])
    assert isinstance(gd_subset, gazedata.GazeData)


def test_subset_complete_cols(gd):

    gd_subset = gd[['time', 'x', 'y']]
    assert numpy.array_equal(gd_subset, constants.ARRAY)
    assert isinstance(gd_subset, gazedata.GazeData)


def test_subset_incomplete_cols(gd):

    gd_subset = gd[['x', 'y']]
    assert numpy.array_equal(gd_subset, constants.ARRAY_XY)
    assert not isinstance(gd_subset, gazedata.GazeData)
