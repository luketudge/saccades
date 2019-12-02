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
    """Rotate coordinates about a point.

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


def velocity(coords):
    """Calculate velocity of coordinates.

    The velocity of a coordinate pair is based on the euclidean distance \
    travelled since the previous coordinate pair. \
    The velocity of the very first coordinate pair is `numpy.nan`.

    :param coords: *(time, x, y)* coordinates with shape *(n, 3)*, \
    where *n* is the number of gaze samples.
    :type coords: :class:`numpy.ndarray` \
    or sequence convertible to :class:`numpy.ndarray`
    :return: Vector of velocities of `coords`.
    :rtype: :class:`numpy.ndarray`
    """

    coords = check_shape(coords, (None, 3))

    diffs = numpy.diff(coords, axis=0)
    distances = numpy.linalg.norm(diffs[:, 1:3], axis=1)
    velocities = distances / diffs[:, 0]

    return numpy.append([numpy.nan], velocities)


def acceleration(t, v):
    """Calculate acceleration.

    The acceleration of a point is based on the \
    difference in velocity since the previous point \
    and the difference in time since the previous point.

    :param t: Vector of times.
    :type t: :class:`numpy.ndarray` \
    or sequence convertible to :class:`numpy.ndarray`
    :param v: Vector of velocities.
    :type v: :class:`numpy.ndarray` \
    or sequence convertible to :class:`numpy.ndarray`
    :return: Vector of accelerations.
    :rtype: :class:`numpy.ndarray`
    """

    t = check_shape(t, (None, ))
    v = check_shape(v, (None, ))

    accelerations = numpy.diff(v) / numpy.diff(t)

    return numpy.append([numpy.nan], accelerations)
