# -*- coding: utf-8 -*-

import numpy


#%% Constants

DEFAULT_SPACE_UNITS = 'px'
"""Assume screen pixels as a default unit for gaze coordinates.
"""


#%% Main class

class GazeArray(numpy.ndarray):
    """Array of gaze data.

    Gaze data has shape *(n, 3)*, \
    where *n* is the number of gaze samples, \
    and the three columns are *time*, \
    *x gaze position*, *y gaze position*.
    """

    def __new__(cls, input_array, time_units=None, space_units=DEFAULT_SPACE_UNITS):
        """Initialize a new GazeArray.

        :param input_array: :class:`numpy.ndarray` \
        (or sequence convertible to :class:`numpy.ndarray`).
        :param time_units: Units of *time* column, \
        as proportion of a second \
        (for example 0.001 for milliseconds).
        :type time_units: `float`
        :param space_units: Units of *x* and *y* columns. \
        Defaults to :data:`DEFAULT_SPACE_UNITS`.
        :type space_units: `str`
        :raises ValueError: If `input_array` does not have \
        exactly 2 dimensions and exactly 3 columns.
        """

        obj = numpy.asarray(input_array).view(cls)

        if obj.ndim != 2:
            msg = 'Input has {} dimensions but 2 required.'
            raise ValueError(msg.format(obj.ndim))

        if obj.shape[1] != 3:
            msg = 'Input has {} columns but 3 required (time, x, y).'
            raise ValueError(msg.format(obj.shape[1]))

        obj.time_units = time_units
        obj.space_units = space_units

        return obj

    def __array_finalize__(self, obj):

        if obj is None:
            return

        self.time_units = getattr(obj, 'time_units', None)
        self.space_units = getattr(obj, 'space_units', DEFAULT_SPACE_UNITS)

        return
