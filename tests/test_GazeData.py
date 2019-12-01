# -*- coding: utf-8 -*-

import numpy
import pandas

from . import constants

from saccades import dataframe


# GazeData methods that wrap functions from other modules
# are tested in the test files for those modules.
# This test file tests the other features of the GazeData class.


#%% __init__()

def test_GazeData_init_types():

    for input_type in [constants.SEQUENCE, constants.ARRAY, constants.DATAFRAME]:
        gd = dataframe.GazeData(input_type)
        assert isinstance(gd, dataframe.GazeData)
        assert isinstance(gd, pandas.DataFrame)
        assert numpy.array_equal(gd, constants.ARRAY)


def test_GazeData_attributes():

    gd = dataframe.GazeData(constants.ARRAY, time_units=constants.TIME_UNITS)

    #assert gd.columns == ('time', 'x', 'y')
    #assert gd.time_units == TIME_UNITS
    #assert gd.space_units == dataframe.DEFAULT_SPACE_UNITS


# Check we get a copy and not a view.
def test_GazeData_is_not_view():

    gd = dataframe.GazeData(constants.ARRAY)
    gd['time'][0] = 9000.

    assert constants.ARRAY[0, 0] != 9000.
