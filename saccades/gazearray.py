# -*- coding: utf-8 -*-
"""
Array class for gaze coordinates.
"""

import numpy


class GazeArray(numpy.ndarray):
    """
    """

    def __new__(cls, input_array):
        """
        """

        obj = numpy.asarray(input_array).view(cls)

        return obj

    def __array_finalize__(self, obj):

        return
