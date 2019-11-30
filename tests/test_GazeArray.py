# -*- coding: utf-8 -*-

import numpy
import pandas
import pytest

from saccades import gazearray


# GazeArray methods that wrap functions from other modules
# are tested in the test files for those modules.
# This test file tests all the other features of the GazeArray class.


#%% Setup

ARRAY = numpy.array([[0., 0., 1.],
                     [1., 2., 3.],
                     [2., 4., 5.]])

TIME_UNITS = 0.001


#%% __new__()

def test_init():

    gazedata_numpy = gazearray.GazeArray(ARRAY)
    gazedata_list = gazearray.GazeArray(list(ARRAY))

    for gd in [gazedata_numpy, gazedata_list]:
        assert isinstance(gd, gazearray.GazeArray)
        assert isinstance(gd, numpy.ndarray)

    assert numpy.array_equal(gazedata_numpy, gazedata_list)


def test_init_from_invalid_shape():

    with pytest.raises(ValueError):
        gazearray.GazeArray(ARRAY[0, :])

    with pytest.raises(ValueError):
        gazearray.GazeArray(ARRAY[:, 1:3])


def test_init_attributes():

    gazedata = gazearray.GazeArray(ARRAY, time_units=TIME_UNITS)

    assert gazedata.columns == gazearray.COLUMN_NAMES[:3]
    assert gazedata.time_units == TIME_UNITS
    assert gazedata.space_units == gazearray.DEFAULT_SPACE_UNITS


#%% to_dataframe()

def test_to_dataframe():

    gazedata = gazearray.GazeArray(ARRAY)
    df = gazedata.to_dataframe()

    assert isinstance(df, pandas.DataFrame)
    assert numpy.array_equal(gazedata, df)
    assert all(df.columns == gazedata.columns)


# Check we get a copy and not a view.
def test_to_dataframe_is_not_view():

    gazedata = gazearray.GazeArray(ARRAY)
    df = gazedata.to_dataframe()
    df[gazearray.COLUMN_NAMES[0]][0] = 9000.

    assert gazedata[0, 0] != 9000.
