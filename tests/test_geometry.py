# -*- coding: utf-8 -*-

import numpy

from . import constants

from saccades import dataframe
from saccades import geometry


# Use numpy.allclose() to allow for floating-point error if necessary.


#%% center()

def test_center():

    observed = geometry.center(constants.ARRAY_XY, constants.ORIGIN)

    assert numpy.array_equal(observed, constants.CENTERED)


def test_center_as_GazeData_method():

    gd = dataframe.GazeData(constants.ARRAY)
    gd.center(constants.ORIGIN)

    assert numpy.array_equal(gd[['x', 'y']], constants.CENTERED)


# Since casting a length-2 vector to a 2x2 array
# could in theory be done either by row or by column,
# and since I always worry that I have read the docs wrong,
# this test helps me sleep at night.
def test_center_with_square_array():

    observed = geometry.center(constants.ARRAY_XY[:2, :], constants.ORIGIN)

    assert numpy.array_equal(observed, constants.CENTERED[:2, :])


#%% rotate()

def test_rotate():

    observed = geometry.rotate(constants.ARRAY_XY, constants.ANGLE)

    assert numpy.allclose(observed, constants.ROTATED)


def test_rotate_about_center():

    observed = geometry.rotate(constants.ARRAY_XY, constants.ANGLE, origin=constants.ORIGIN)

    assert numpy.allclose(observed, constants.CENTER_ROTATED)


def test_rotate_as_GazeData_method():

    gd = dataframe.GazeData(constants.ARRAY)
    gd.rotate(constants.ANGLE)

    assert numpy.allclose(gd[['x', 'y']], constants.ROTATED)
