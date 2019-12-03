# -*- coding: utf-8 -*-
"""Miscellaneous tools.
"""

import numpy


def blockmanager_to_array(blockmanager):

    # The .as_array() method is new to pandas v0.23.
    # Revert to the older .as_matrix() method if it fails.
    try:
        return blockmanager.as_array().transpose()
    except AttributeError:
        return blockmanager.as_matrix().transpose()


def check_shape(array, shape):
    """Check that an array is of an expected shape.

    :param array: Array to check.
    :type array: :class:`numpy.ndarray` \
    or sequence convertible to :class:`numpy.ndarray`
    :param shape: Expected shape. \
    Occurrences of `None` indicate that a dimension may be of any size. \
    So for example `(None, 3)` allows for an *(n, 3)* array \
    for any value of *n*.
    :type shape: `tuple`
    :return: `array`, converted to :class:`numpy.ndarray`.
    :rtype: :class:`numpy.ndarray`
    :raises ValueError: If `array` is not of the expected shape.
    """

    # numpy.array returns a copy not a view, so this should be ok.
    array = numpy.array(array)

    if array.ndim != len(shape):
        msg = 'Array has {} dimensions but {} required.'
        raise ValueError(msg.format(array.ndim, len(shape)))

    for obs, exp in zip(array.shape, shape):
        if (exp is not None) and (obs != exp):
            msg = 'Array has shape {} but {} required.'
            raise ValueError(msg.format(array.shape, shape))

    return array
