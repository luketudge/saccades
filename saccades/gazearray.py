# -*- coding: utf-8 -*-
"""Module providing classes for representing gaze coordinates.
"""

import numpy
import pandas

from .geometry import center
from .geometry import rotate
from .tools import check_shape


#%% Constants

COLUMN_NAMES = ['time', 'x', 'y']
"""Order of columns for GazeArray.
"""

DEFAULT_SPACE_UNITS = 'px'
"""Assume screen pixels as a default unit for gaze coordinates.
"""


#%% Main class

class GazeArray(numpy.ndarray):
    """Array of gaze data.

    Mainly just a :class:`numpy.ndarray` \
    with some extra methods for processing gaze data, \
    most of which wrap functions from :py:mod:`.geometry`.
    """

    def __new__(cls, input_array, time_units=None, space_units=DEFAULT_SPACE_UNITS):
        """Initialize a new GazeArray.

        :param input_array: Array of *(t, x, y)* \
        coordinates with shape *(n, 3)*, \
        where *n* is the number of gaze samples, \
        and the three columns are *time*, \
        *x gaze position*, *y gaze position*.
        :type input_array: :class:`numpy.ndarray` \
        or sequence convertible to :class:`numpy.ndarray`
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

        check_shape(input_array, (None, 3))

        obj = numpy.asarray(input_array).view(cls)

        obj.columns = COLUMN_NAMES[:3]
        obj.time_units = time_units
        obj.space_units = space_units

        return obj

    def __array_finalize__(self, obj):

        # Not completely sure this clause is necessary for our purposes.
        # Currently it ends up being the only line without test coverage.
        # But just in case.
        # REF: https://docs.scipy.org/doc/numpy/user/basics.subclassing.html
        if obj is None:
            return

        self.columns = getattr(obj, 'columns', COLUMN_NAMES[:3])
        self.time_units = getattr(obj, 'time_units', None)
        self.space_units = getattr(obj, 'space_units', DEFAULT_SPACE_UNITS)

    def center(self, origin):
        """Center gaze coordinates on a new origin.

        See :func:`.geometry.center`.
        """

        self[:, 1:3] = center(self[:, 1:3], origin)

    def rotate(self, theta, origin=(0, 0)):
        """Rotate gaze coordinates.

        See :func:`.geometry.rotate`.
        """

        self[:, 1:3] = rotate(self[:, 1:3], theta, origin)

    def to_dataframe(self):
        """Convert gaze data to pandas DataFrame.

        :rtype: :class:`pandas.DataFrame`
        """

        return pandas.DataFrame(self, columns=self.columns, copy=True)
