# -*- coding: utf-8 -*-

import numpy

from saccades import gazearray
from saccades import geometry


# Use numpy.allclose() to account for floating-point error where necessary.


#%% Setup

ARRAY = [[0., 1.],
         [2., 3.],
         [4., 5.]]

GAZEARRAY = [[i] + row for i, row in enumerate(ARRAY)]

ORIGIN = (1., 2.)

CENTERED = [[-1., -1.],
            [1., 1.],
            [3., 3.]]

ANGLE = numpy.pi / 2

ROTATED = [[-1., 0.],
           [-3., 2.],
           [-5., 4.]]

CENTER_ROTATED = [[2., 1.],
                  [0., 3.],
                  [-2., 5.]]


#%% center()

def test_center():

    observed = geometry.center(ARRAY, ORIGIN)

    assert numpy.array_equal(observed, CENTERED)


def test_center_as_GazeArray_method():

    gazedata = gazearray.GazeArray(GAZEARRAY)
    gazedata.center(ORIGIN)

    assert numpy.array_equal(gazedata[:, 1:3], CENTERED)


# Since casting a length-2 vector to a 2x2 array
# could in theory be done either by row or by column,
# and since I always worry that I have read the docs wrong,
# this test helps me sleep at night.
def test_center_with_square_array():

    observed = geometry.center(ARRAY[:2], ORIGIN)

    assert numpy.array_equal(observed, CENTERED[:2])


#%% rotate()

def test_rotate():

    observed = geometry.rotate(ARRAY, ANGLE)

    assert numpy.allclose(observed, ROTATED)


def test_rotate_about_center():

    observed = geometry.rotate(ARRAY, ANGLE, origin=ORIGIN)

    assert numpy.allclose(observed, CENTER_ROTATED)


def test_rotate_as_GazeArray_method():

    gazedata = gazearray.GazeArray(GAZEARRAY)
    gazedata.rotate(ANGLE)

    assert numpy.allclose(gazedata[:, 1:3], ROTATED)
