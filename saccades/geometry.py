# -*- coding: utf-8 -*-
"""Various geometry functions for working with gaze coordinates.
"""

from .tools import check_shape


def center(coords, origin):
    """Translate coordinates to center them on a new origin.

    :param coords: *(x, y)* coordinates with shape *(n, 2)*, \
    where *n* is the number of gaze samples.
    :type coords: :class:`numpy.ndarray` \
    or sequence convertible to :class:`numpy.ndarray`.
    :param origin: *(x, y)* coordinates of new origin, \
    with shape *(1, 2)*.
    :type origin: :class:`numpy.ndarray` \
    or sequence convertible to :class:`numpy.ndarray`.
    :return: Recentered `coords`.
    :rtype: :class:`numpy.ndarray`
    """

    coords = check_shape(coords, (None, 2))
    origin = check_shape(origin, (2,))

    return coords - origin
