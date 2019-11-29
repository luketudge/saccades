# -*- coding: utf-8 -*-
"""Various geometry functions for working with gaze coordinates.
"""

import numpy

from .tools import check_shape


def center(coords, origin):
    """Translate coordinates to center them on a new origin.

    :param coords: *(x, y)* coordinates with shape *(n, 2)*, \
    where *n* is the number of gaze samples.
    :type coords: :class:`numpy.ndarray` \
    or sequence convertible to :class:`numpy.ndarray`
    :param origin: *(x, y)* coordinates of new origin.
    :type origin: :class:`numpy.ndarray` \
    or sequence convertible to :class:`numpy.ndarray`
    :return: Recentered `coords`.
    :rtype: :class:`numpy.ndarray`
    """

    coords = check_shape(coords, (None, 2))
    origin = check_shape(origin, (2,))

    return coords - origin


def rotate(coords, theta, origin=(0, 0)):
    """Rotate coordinates.

    :param coords: *(x, y)* coordinates with shape *(n, 2)*, \
    where *n* is the number of gaze samples.
    :type coords: :class:`numpy.ndarray` \
    or sequence convertible to :class:`numpy.ndarray`
    :param theta: Angle of counterclockwise rotation, in radians.
    :type theta: `float`
    :param origin: *(x, y)* coordinates of origin \
    about which to rotate.
    :type origin: :class:`numpy.ndarray` \
    or sequence convertible to :class:`numpy.ndarray`
    :return: Rotated `coords`.
    :rtype: :class:`numpy.ndarray`
    """

    coords = center(coords, origin)

    c = numpy.cos(theta)
    s = numpy.sin(theta)
    rotation_matrix = numpy.array([[c, s], [-s, c]])

    coords = numpy.matmul(coords, rotation_matrix)

    return coords + origin
