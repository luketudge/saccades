# -*- coding: utf-8 -*-

import numpy

from saccades import gazearray
from saccades import geometry


#%% Setup

ARRAY = [[0, 1],
         [2, 3],
         [4, 5]]

GAZEARRAY = [[i] + row for i, row in enumerate(ARRAY)]

ORIGIN = (1, 2)

CENTERED = [[-1, -1],
            [1, 1],
            [3, 3]]


#%% center()

def test_center():

    observed = geometry.center(ARRAY, ORIGIN)

    assert numpy.array_equal(observed, CENTERED)


def test_center_as_GazeArray_method():

    gazedata = gazearray.GazeArray(GAZEARRAY)
    gazedata.center(ORIGIN)

    assert numpy.array_equal(gazedata[:, 1:3], CENTERED)
