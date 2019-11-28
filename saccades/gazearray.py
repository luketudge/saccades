# -*- coding: utf-8 -*-
"""
A class for working with gaze coordinates.
"""

import numpy


DEFAULT_TIME_UNIT = 's'
DEFAULT_SPACE_UNIT = 'px'


class GazeArray(numpy.ndarray):
    """Array of gaze data.

    Inherits from ``numpy.ndarray``.

    Gaze data has shape `(n, 3)`, \
    where ``n`` is the number of gaze samples, \
    and the three columns are \
    *time*, *x*, *y*.
    """

    def __new__(cls, input_array, center=None, target=None,
                time_units=DEFAULT_TIME_UNIT,
                space_units=DEFAULT_SPACE_UNIT):
        """Initialize a new GazeArray.

        :param input_array: ``numpy.ndarray`` \
        (or sequence convertible to ``numpy.ndarray``).
        :raises ValueError: ``input_array`` \
        does not have exactly 2 dimensions \
        and exactly 3 columns.
        """

        obj = numpy.asarray(input_array).view(cls)

        if obj.ndim != 2:
            msg = 'Input has {} dimensions but 2 required.'
            raise ValueError(msg.format(obj.ndim))

        if obj.shape[1] != 3:
            msg = 'Input has {} columns but 3 required (time, x, y).'
            raise ValueError(msg.format(obj.shape[1]))

        obj.center = center
        obj.target = target
        obj.time_units = time_units

        return obj

    def __array_finalize__(self, obj):

        if obj is None:
            return

        self.center = getattr(obj, 'center', None)
        self.target = getattr(obj, 'target', None)
        self.time_units = getattr(obj, 'time_units', DEFAULT_TIME_UNIT)
        self.space_units = getattr(obj, 'space_units', DEFAULT_SPACE_UNIT)

        return
