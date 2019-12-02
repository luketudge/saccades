# -*- coding: utf-8 -*-

import numpy
import pandas


#%% Input types

# Probably most often we will have to initialize from a numpy.ndarray,
# following a call to numpy.genfromtxt().
# So most test functions begin by initializing from ARRAY.

SEQUENCE = [[2., 1., 0.],
            [4., 4., 4.],
            [6., 10., 12.]]

ARRAY = numpy.array(SEQUENCE)
ARRAY_XY = numpy.array(ARRAY[:, 1:3])

DATAFRAME = pandas.DataFrame(ARRAY,
                             columns=('time', 'x', 'y'),
                             copy=True)


#%% Attributes

SHAPE = (3, 3)


#%% Transformations

ORIGIN = (1., 2.)

CENTERED = numpy.array([[0., -2.],
                        [3., 2.],
                        [9., 10.]])

ANGLE = numpy.pi / 2

ROTATED = numpy.array([[0., 1.],
                       [-4., 4.],
                       [-12., 10.]])

CENTER_ROTATED = numpy.array([[3., 2.],
                              [-1., 5.],
                              [-9., 11.]])
