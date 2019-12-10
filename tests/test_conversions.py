# -*- coding: utf-8 -*-

import numpy

from . import constants

from saccades import conversions


# Use numpy.allclose() in place of numpy.array_equal()
# to allow for floating-point error where necessary.


#%% _viewing_dist_to_px()

def test_viewing_dist_to_px():

    result = conversions._viewing_dist_to_px(constants.VIEWING_DIST,
                                             screen_res=constants.SCREEN_RES,
                                             screen_diag=constants.SCREEN_DIAG)

    assert result == constants.VIEWING_DIST_PX


#%% px_to_dva()

def test_px_to_dva_scalar():

    result = conversions.px_to_dva(constants.PX[0],
                                   screen_res=constants.SCREEN_RES,
                                   screen_diag=constants.SCREEN_DIAG,
                                   viewing_dist=constants.VIEWING_DIST)

    assert numpy.allclose(result, constants.DVA[0])


def test_px_to_dva_vector():

    result = conversions.px_to_dva(constants.PX,
                                   screen_res=constants.SCREEN_RES,
                                   screen_diag=constants.SCREEN_DIAG,
                                   viewing_dist=constants.VIEWING_DIST)

    assert numpy.allclose(result, constants.DVA)


#%% dva_to_px()

def test_dva_to_px_scalar():

    result = conversions.dva_to_px(constants.DVA[0],
                                   screen_res=constants.SCREEN_RES,
                                   screen_diag=constants.SCREEN_DIAG,
                                   viewing_dist=constants.VIEWING_DIST)

    assert numpy.allclose(result, constants.PX[0])


def test_dva_to_px_vector():

    result = conversions.dva_to_px(constants.DVA,
                                   screen_res=constants.SCREEN_RES,
                                   screen_diag=constants.SCREEN_DIAG,
                                   viewing_dist=constants.VIEWING_DIST)

    assert numpy.allclose(result, constants.PX)
