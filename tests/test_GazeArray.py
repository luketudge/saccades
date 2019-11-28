# -*- coding: utf-8 -*-

from os import path

import numpy
import pytest

from saccades import gazearray


#%% Setup

DATA_FILENAME = 'example.csv'
DATA_PATH = path.join(path.dirname(path.abspath(__file__)), 'data', DATA_FILENAME)

COORDS = numpy.genfromtxt(DATA_PATH, delimiter=',')
SCREEN_CENTER = (320, 240)
TIME_UNITS = 'ms'


#%% __new__()

def test_new_from_numpy_array():

    gazedata = gazearray.GazeArray(COORDS)

    assert isinstance(gazedata, gazearray.GazeArray)


def test_new_from_sequence():

    coords_list = list(COORDS)
    gazedata = gazearray.GazeArray(coords_list)

    assert isinstance(gazedata, gazearray.GazeArray)


def test_new_from_invalid_shape():

    with pytest.raises(ValueError):
        gazearray.GazeArray([0, 1, 2])

    with pytest.raises(ValueError):
        gazearray.GazeArray(COORDS[:, 1:])


def test_new_attributes():

    gazedata = gazearray.GazeArray(COORDS,
                                   center=SCREEN_CENTER,
                                   time_units=TIME_UNITS)

    assert gazedata.center == SCREEN_CENTER
    assert gazedata.target is None
    assert gazedata.time_units == TIME_UNITS
    assert gazedata.space_units == gazearray.DEFAULT_SPACE_UNIT
