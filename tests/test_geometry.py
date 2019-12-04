# -*- coding: utf-8 -*-

import numpy

from . import constants

from saccades import geometry


# Use numpy.allclose() in place of numpy.array_equal()
# to allow for floating-point error where necessary.

# numpy.array_equal() returns False in the presence of any NaN values,
# whereas numpy.allclose() allows comparing NaN values as equal,
# So also use numpy.allclose() when results are expected to contain NaN.
# https://github.com/numpy/numpy/issues/9229


#%% center()

def test_center():

    centered = geometry.center(constants.ARRAY_XY, constants.ORIGIN)

    assert numpy.array_equal(centered, constants.CENTERED)


def test_center_as_GazeData_method(gd):

    gd.center(constants.ORIGIN)

    assert numpy.array_equal(gd[['x', 'y']], constants.CENTERED)


# Since casting a length-2 vector to a 2x2 array
# could in theory be done either by row or by column,
# and since I always worry that I have read the docs wrong,
# this test helps me sleep at night.
def test_center_with_square_array():

    centered = geometry.center(constants.ARRAY_XY[:2, :], constants.ORIGIN)

    assert numpy.array_equal(centered, constants.CENTERED[:2, :])


#%% rotate()

def test_rotate():

    rotated = geometry.rotate(constants.ARRAY_XY, constants.ANGLE)

    assert numpy.allclose(rotated, constants.ROTATED)


def test_rotate_about_center():

    rotated = geometry.rotate(constants.ARRAY_XY,
                              constants.ANGLE,
                              origin=constants.ORIGIN)

    assert numpy.allclose(rotated, constants.CENTER_ROTATED)


def test_rotate_as_GazeData_method(gd):

    gd.rotate(constants.ANGLE)

    assert numpy.allclose(gd[['x', 'y']], constants.ROTATED)


#%% velocity()

def test_velocity():

    velocity = geometry.velocity(constants.ARRAY)

    assert numpy.allclose(velocity, constants.VELOCITY, equal_nan=True)


def test_velocity_as_GazeData_method(gd):

    gd.get_velocities()

    assert numpy.allclose(gd['velocity'], constants.VELOCITY, equal_nan=True)


#%% acceleration()

def test_acceleration():

    acceleration = geometry.acceleration(constants.ARRAY[:, 0],
                                         constants.VELOCITY)

    assert numpy.allclose(acceleration, constants.ACCELERATION, equal_nan=True)


def test_acceleration_as_GazeData_method(gd):

    gd.get_accelerations()

    observed = gd['acceleration']

    assert numpy.allclose(observed, constants.ACCELERATION, equal_nan=True)

    # Check also that the intermediate velocity column was created.
    assert 'velocity' in gd


def test_acceleration_as_GazeData_method_with_existing_velocities(gd):

    # Dummy velocity column filled with zeros.
    velocities = numpy.zeros_like(constants.VELOCITY)
    gd['velocity'] = velocities

    gd.get_accelerations()

    expected = numpy.append([numpy.nan], velocities[1:])

    assert numpy.allclose(gd['acceleration'], expected, equal_nan=True)
