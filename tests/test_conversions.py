# -*- coding: utf-8 -*-
"""Test the conversion functions.

Also test them as methods of the GazeData class.
"""

import numpy

from . import helpers

from saccades import conversions


# %% _viewing_dist_to_px()

def test_viewing_dist_to_px(vd2px):
    """Test converting viewing distance to pixels.
    """

    result = conversions._viewing_dist_to_px(vd2px['in']['dist'],
                                             screen_res=vd2px['in']['res'],
                                             screen_diag=vd2px['in']['diag'])

    assert result == vd2px['out']['px']


# %% px_to_dva()

def test_px_to_dva(px2dva):
    """Test converting pixels to degrees of visual angle.
    """

    result = conversions.px_to_dva(px2dva['in']['px'],
                                   screen_res=px2dva['in']['res'],
                                   screen_diag=px2dva['in']['diag'],
                                   viewing_dist=px2dva['in']['dist'])

    assert numpy.array_equal(result, px2dva['out']['dva'])


def test_px_to_dva_as_GazeData_method(gaze_data_1, px2dva):
    """Test converting pixels to degrees of visual angle
    as a method of the GazeData class.
    """

    gd = helpers.init_gazedata(gaze_data_1,
                               screen_res=px2dva['in']['res'],
                               screen_diag=px2dva['in']['diag'],
                               viewing_dist=px2dva['in']['dist'])
    result = gd.px_to_dva(px2dva['in']['px'])

    assert numpy.array_equal(result, px2dva['out']['dva'])


# %% dva_to_px()

def test_dva_to_px(px2dva):
    """Test converting degrees of visual angle to pixels.
    """

    result = conversions.dva_to_px(px2dva['in']['dva'],
                                   screen_res=px2dva['in']['res'],
                                   screen_diag=px2dva['in']['diag'],
                                   viewing_dist=px2dva['in']['dist'])

    assert numpy.allclose(result, px2dva['out']['px'])


def test_dva_to_px_as_GazeData_method(gaze_data_1, px2dva):
    """Test converting degrees of visual angle to pixels
    as a method of the GazeData class.
    """

    gd = helpers.init_gazedata(gaze_data_1,
                               screen_res=px2dva['in']['res'],
                               screen_diag=px2dva['in']['diag'],
                               viewing_dist=px2dva['in']['dist'])
    result = gd.dva_to_px(px2dva['in']['dva'])

    assert numpy.allclose(result, px2dva['out']['px'])
