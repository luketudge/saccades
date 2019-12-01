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


def test_GazeData_attributes():

    gd = gazedata.GazeData(constants.ARRAY, time_units=constants.TIME_UNITS)

    assert list(gd.columns) == ['time', 'x', 'y']
    assert gd.time_units == constants.TIME_UNITS
    assert gd.space_units == 'px'


# Check we get a copy and not a view.
def test_GazeData_is_not_view():

    gd = gazedata.GazeData(constants.ARRAY)
    gd['time'][0] = 9000.

    assert constants.ARRAY[0, 0] != 9000.


#%% pandas.DataFrame

# Check that the most useful pandas.DataFrame functionality is preserved.

def test_subset():

    gd = gazedata.GazeData(constants.ARRAY)
    gd_subset = gd[:2]
    assert isinstance(gd_subset, gazedata.GazeData)
    assert isinstance(gd_subset, pandas.DataFrame)
