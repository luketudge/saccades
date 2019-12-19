# -*- coding: utf-8 -*-

import numpy

from . import constants

from saccades import conversions


# Use numpy.allclose() in place of numpy.array_equal()
# to allow for floating-point error where necessary.


# %% _viewing_dist_to_px()

def test_viewing_dist_to_px():

    result = conversions._viewing_dist_to_px(constants.VIEWING_DIST,
                                             screen_res=constants.SCREEN_RES,
                                             screen_diag=constants.SCREEN_DIAG)

    assert result == constants.VIEWING_DIST_PX


# %% px_to_dva()

def test_px_to_dva():

    result = conversions.px_to_dva(constants.PX,
                                   screen_res=constants.SCREEN_RES,
                                   screen_diag=constants.SCREEN_DIAG,
                                   viewing_dist=constants.VIEWING_DIST)

    assert numpy.allclose(result, constants.DVA)


def test_px_to_dva_as_GazeData_method(gd):

    result = gd.px_to_dva(constants.PX)

    assert numpy.allclose(result, constants.DVA)


# %% dva_to_px()

def test_dva_to_px():

    result = conversions.dva_to_px(constants.DVA,
                                   screen_res=constants.SCREEN_RES,
                                   screen_diag=constants.SCREEN_DIAG,
                                   viewing_dist=constants.VIEWING_DIST)

    assert numpy.allclose(result, constants.PX)


def test_dva_to_px_as_GazeData_method(gd):

    result = gd.dva_to_px(constants.DVA)

    assert numpy.allclose(result, constants.PX)
