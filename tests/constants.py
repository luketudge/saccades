# -*- coding: utf-8 -*-

import numpy
import pandas


#%% Input types

# Probably most often we will have to initialize from a numpy.ndarray,
# following a call to numpy.genfromtxt().
# So most test functions begin by initializing from ARRAY.

SEQUENCE = [[0., 0., 1.],
            [1., 2., 3.],
            [2., 4., 5.]]

ARRAY = numpy.array(SEQUENCE)

DATAFRAME = pandas.DataFrame(ARRAY,
                             columns=('time', 'x', 'y'),
                             copy=True)


#%% Attributes

SHAPE = (3, 3)


#%% Transformations

ARRAY_XY = numpy.array(ARRAY[:, 1:3])

ORIGIN = (1., 2.)

CENTERED = numpy.array([[-1., -1.],
                        [1., 1.],
                        [3., 3.]])

ANGLE = numpy.pi / 2

ROTATED = numpy.array([[-1., 0.],
                       [-3., 2.],
                       [-5., 4.]])

CENTER_ROTATED = numpy.array([[2., 1.],
                              [0., 3.],
                              [-2., 5.]])
