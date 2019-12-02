# -*- coding: utf-8 -*-
"""Module providing classes for representing gaze coordinates.
"""

import pandas

from .geometry import center
from .geometry import rotate
from .geometry import velocity
from .tools import check_shape
from .tools import blockmanager_to_array


#%% Constants

INIT_COLUMNS = ['time', 'x', 'y']


#%% Main class

class GazeData(pandas.DataFrame):
    """Table of gaze data.

    A :class:`pandas.DataFrame` \
    with some extra methods for processing gaze data. \
    Most methods wrap functions from :py:mod:`.geometry`.
    """

    # pandas.DataFrame treats attributes as column names.
    # (This is one of the minor irritations of working with pandas;
    # it doesn't stick to *one* correct and intuitive method of indexing.)
    # So we must declare custom attributes here to avoid them being treated as columns.
    # (Not yet implemented, but just in case.)
    # https://pandas.pydata.org/pandas-docs/stable/development/extending.html#define-original-properties
    # _internal_names = pandas.DataFrame._internal_names + []
    # _internal_names_set = set(_internal_names)

    def __new__(cls, data):

        # When a new instance of the custom class is requested,
        # this can be for two different reasons:
        # (1) A completely new instance is being initialized.
        # (2) A new instance is being initialized from a subset of an existing instance.

        # We can detect (2) with the following clause.
        # But this is unfortunately not part of the pandas public API,
        # so we may have to watch out for changes in later pandas versions.
        # https://github.com/pandas-dev/pandas/blob/master/pandas/core/internals/managers.py
        if isinstance(data, pandas.core.internals.BlockManager):

            # A subset might still be a full valid table of gaze data,
            # if it contains the 3 essential columns 'time', 'x', and 'y'.
            # So if this is the case, we initialize an instance of the custom class.
            if list(data.items)[:3] == INIT_COLUMNS:
                return super().__new__(cls)

            # Otherwise we initialize a standard pandas DataFrame.
            # This needs the array form of the data.
            return pandas.DataFrame(blockmanager_to_array(data))

        # And this handles (1).
        data = check_shape(data, (None, 3))
        return super().__new__(cls)

    def __init__(self, data):
        """:param data: Gaze data with shape *(n, 3)*, \
        where *n* is the number of gaze samples, \
        and columns are *time*, *x gaze position*, *y gaze position*.
        :type data: :class:`numpy.ndarray` \
        or convertible to :class:`numpy.ndarray`
        """

        super().__init__(data=data, columns=INIT_COLUMNS, copy=True)

    # To allow subsets of the custom class to preserve their type,
    # we need to override the constructor that subsetting calls.
    # Otherwise it will still call pandas.DataFrame.
    # https://pandas.pydata.org/pandas-docs/stable/development/extending.html#override-constructor-properties
    @property
    def _constructor(self):
        return GazeData

    def center(self, origin):
        """Center gaze coordinates.

        See :func:`.geometry.center`.
        """

        self[['x', 'y']] = center(self[['x', 'y']], origin)

    def rotate(self, theta, origin=(0., 0.)):
        """Rotate gaze coordinates.

        See :func:`.geometry.rotate`.
        """

        self[['x', 'y']] = rotate(self[['x', 'y']], theta, origin)

    def get_velocities(self):
        """Calculate velocity of gaze coordinates.

        Velocities are added as a new column.

        See :func:`.geometry.velocity`.
        """

        self['velocity'] = velocity(self[['time', 'x', 'y']])
