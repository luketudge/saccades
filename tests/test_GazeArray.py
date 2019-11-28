# -*- coding: utf-8 -*-

from os import path

import numpy

from saccades.gazearray import GazeArray


#%% Setup

DATA_FILENAME = 'example.csv'
DATA_PATH = path.join(path.dirname(path.abspath(__file__)), 'data', DATA_FILENAME)
COORDS = numpy.genfromtxt(DATA_PATH, delimiter=',')

EXPECTED_SHAPE = (148, 3)


#%% Tests

def test_GazeArray_from_numpy_array():
    
    gazedata = GazeArray(COORDS)
    assert isinstance(gazedata, GazeArray)


def test_GazeArray_from_sequence():
    
    coords_list = list(COORDS)
    assert isinstance(coords_list, list)
    
    gazedata = GazeArray(coords_list)
    assert isinstance(gazedata, GazeArray)
