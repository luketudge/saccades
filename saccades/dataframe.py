# -*- coding: utf-8 -*-
"""Module providing classes for representing gaze coordinates.
"""

import numpy
import pandas

from .geometry import center
from .geometry import rotate
from .tools import check_shape


#%% Constants

DEFAULT_SPACE_UNITS = 'px'
"""Assume screen pixels as a default unit for gaze coordinates.
"""


#%% Main class

class GazeData(pandas.DataFrame):
    """Table of gaze data.

    Mainly just a :class:`pandas.DataFrame` \
    with some extra methods for processing gaze data, \
    most of which wrap functions from :py:mod:`.geometry`.
    """

    def __init__(self, data, time_units=None, space_units=DEFAULT_SPACE_UNITS):
        """
        """

        data = check_shape(data, (None, 3))

        super().__init__(data=data, columns=['time', 'x', 'y'], copy=True)

    # Ensures that subsetting and other operations preserve GazeData type.
    @property
    def _constructor(self):
        return GazeData

    def center(self, origin):
        """Center gaze coordinates on a new origin.

        See :func:`.geometry.center`.
        """

    def rotate(self, theta, origin=(0., 0.)):
        """Rotate gaze coordinates.

        See :func:`.geometry.rotate`.
        """
