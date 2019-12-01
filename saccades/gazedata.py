# -*- coding: utf-8 -*-
"""Module providing classes for representing gaze coordinates.
"""

import pandas

from .geometry import center
from .geometry import rotate
from .tools import check_shape


#%% Constants

INIT_COLUMNS = ['time', 'x', 'y']


#%% Main class

class GazeData(pandas.DataFrame):
    """Table of gaze data.

    A :class:`pandas.DataFrame` \
    with some extra methods for processing gaze data. \
    Most methods wrap functions from :py:mod:`.geometry`.
    """

    # https://pandas.pydata.org/pandas-docs/stable/development/extending.html#define-original-properties
    _internal_names = pandas.DataFrame._internal_names + ['time_units', 'space_units']
    _internal_names_set = set(_internal_names)

    def __init__(self, data, time_units=None, space_units='px'):
        """:param data: Gaze data with shape *(n, 3)*, \
        where *n* is the number of gaze samples, \
        and columns are *time*, *x gaze position*, *y gaze position*.
        :type data: :class:`numpy.ndarray` \
        or convertible to :class:`numpy.ndarray`
        :param time_units: Units of *time* column, \
        in fractions of a second (e.g. `0.001` for milliseconds).
        :type time_units: `float`
        :param space_units: Units of *x* and *y* columns, \
        for example `'px'` or `'cm'`.
        :type space_units: `str`
        """

        data = check_shape(data, (None, 3))

        self.time_units = time_units
        self.space_units = space_units

        super().__init__(data=data, columns=INIT_COLUMNS, copy=True)

    def center(self, origin):
        """Center gaze coordinates on a new origin.

        See :func:`.geometry.center`.
        """

        self[['x', 'y']] = center(self[['x', 'y']], origin)

    def rotate(self, theta, origin=(0., 0.)):
        """Rotate gaze coordinates.

        See :func:`.geometry.rotate`.
        """

        self[['x', 'y']] = rotate(self[['x', 'y']], theta, origin)
