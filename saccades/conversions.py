# -*- coding: utf-8 -*-
"""Functions for converting between various measurement systems.
"""

import numpy


def _viewing_dist_to_px(viewing_dist, screen_res, screen_diag):

    screen_diag_px = numpy.hypot(*screen_res)
    px_per_dist_unit = screen_diag_px / screen_diag

    return viewing_dist * px_per_dist_unit


def px_to_dva(px, screen_res, screen_diag, viewing_dist):
    """Convert screen pixels to degrees of visual angle.

    :param px: Pixel value(s).
    :type px: scalar or array-like
    :param screen_res: *(x, y)* pixel screen resolution.
    :type screen_res: tuple
    :param screen_diag: Diagonal size of screen, \
    in the same units as `viewing_dist`.
    :type screen_diag: float
    :param viewing_dist: Distance of eye from screen, \
    in the same units as `screen_diag`.
    :type viewing_dist: float
    :return: `px` in degrees of visual angle.
    :rtype: float
    """

    viewing_dist_px = _viewing_dist_to_px(viewing_dist,
                                          screen_res=screen_res,
                                          screen_diag=screen_diag)

    rva = numpy.arctan(px / viewing_dist_px)

    return numpy.degrees(rva)


def dva_to_px(dva, screen_res, screen_diag, viewing_dist):
    """Convert degrees of visual angle to screen pixels.

    :param dva: Degree value(s).
    :type dva: scalar or array-like
    :param screen_res: *(x, y)* pixel screen resolution.
    :type screen_res: tuple
    :param screen_diag: Diagonal size of screen, \
    in the same units as `viewing_dist`.
    :type screen_diag: float
    :param viewing_dist: Distance of eye from screen, \
    in the same units as `screen_diag`.
    :type viewing_dist: float
    :return: `px` in degrees of visual angle.
    :rtype: float
    """

    viewing_dist_px = _viewing_dist_to_px(viewing_dist,
                                          screen_res=screen_res,
                                          screen_diag=screen_diag)

    rva = numpy.radians(dva)

    return numpy.tan(rva) * viewing_dist_px
