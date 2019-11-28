# -*- coding: utf-8 -*-

import numpy


#%% Constants

DEFAULT_TIME_UNIT = 's'
"""Assume seconds as a default time unit. \
But this is really only a placeholder, \
as most eyetracking devices variously use either \
milliseconds or microseconds.
"""

DEFAULT_SPACE_UNIT = 'px'
"""Assume screen pixels as a default space unit. \
This is a good guess for most eyetracking data outputs.
"""


#%% Main class

class GazeArray(numpy.ndarray):
    """Array of gaze data.

    Gaze data has shape *(n, 3)*, \
    where *n* is the number of gaze samples, \
    and the three columns are *time*, *x*, *y*.
    """

    def __new__(cls, input_array, center=None, target=None,
                time_units=DEFAULT_TIME_UNIT,
                space_units=DEFAULT_SPACE_UNIT):
        """Initialize a new GazeArray.

        :param input_array: :class:`numpy.ndarray` \
        (or sequence convertible to :class:`numpy.ndarray`).
        :param center: (x, y) coordinates of screen center.
        :param target: (x, y) coordinates of the main point of interest, \
        for example an image on the screen that may be a target for a saccade.
        :param time_units: Units of *time* column, \
        defaults to :data:`DEFAULT_TIME_UNIT`.
        :param space_units: Units of *x* and *y* columns, \
        defaults to :data:`DEFAULT_SPACE_UNIT`.
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
