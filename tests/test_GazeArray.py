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
TIME_UNITS = 0.001


#%% __new__()

def test_init_from_numpy_array():

    gazedata = gazearray.GazeArray(COORDS)

    assert isinstance(gazedata, gazearray.GazeArray)
    assert isinstance(gazedata, numpy.ndarray)


def test_init_from_sequence():

    gazedata = gazearray.GazeArray(COORDS)
    coords_list = list(COORDS)
    gazedata_list = gazearray.GazeArray(coords_list)

    assert numpy.array_equal(gazedata_list, gazedata)


def test_init_from_invalid_shape():

    with pytest.raises(ValueError):
        gazearray.GazeArray([0, 1, 2])

    with pytest.raises(ValueError):
        gazearray.GazeArray(COORDS[:, 1:3])


def test_init_attributes():

    gazedata = gazearray.GazeArray(COORDS, time_units=TIME_UNITS)

    assert gazedata.time_units == TIME_UNITS
    assert gazedata.space_units == gazearray.DEFAULT_SPACE_UNITS


#%% center()

def test_center():

    gazedata = gazearray.GazeArray(COORDS)
    gazedata.center(SCREEN_CENTER)
