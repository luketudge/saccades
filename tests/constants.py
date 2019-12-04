# -*- coding: utf-8 -*-

import os

import numpy
import pandas


#%% Data

DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')


#%% Valid init types

# These are parametrized in conftest.py.

SEQUENCE = [[2., 1., 0.],
            [4., 4., 4.],
            [6., 10., 12.]]

ARRAY = numpy.array(SEQUENCE)

DF = pandas.DataFrame(ARRAY,
                      columns=('time', 'x', 'y'),
                      copy=True)

DF_CORRECT_SHAPE = DF.copy()
DF_CORRECT_SHAPE.columns = ['a', 'b', 'c']

DF_EXTRA_COLUMN = DF.copy()
DF_EXTRA_COLUMN['foo'] = 'foo'

DF_REORDERED_COLUMNS = DF_EXTRA_COLUMN.copy()
DF_REORDERED_COLUMNS = DF_REORDERED_COLUMNS[['foo', 'y', 'time', 'x']]

STANDARD_INIT_TYPES = [SEQUENCE,
                       ARRAY,
                       DF,
                       DF_CORRECT_SHAPE]

VALID_INIT_TYPES = [SEQUENCE,
                    ARRAY,
                    DF,
                    DF_CORRECT_SHAPE,
                    DF_EXTRA_COLUMN,
                    DF_REORDERED_COLUMNS]

# Give these ones names because they are parametrized into many tests.
VALID_INIT_TYPE_NAMES = ['seq',
                         'arr',
                         'df',
                         'df_shape_only',
                         'df_extra_col',
                         'df_reordered']


#%% Invalid init types

ARRAY_XY = numpy.array(ARRAY[:, 1:3])

DF_XY = pandas.DataFrame(ARRAY_XY,
                         columns=('x', 'y'),
                         copy=True)

DF_INVALID_COLUMNS = DF_EXTRA_COLUMN.copy()
DF_INVALID_COLUMNS.columns = ['x', 'y', 'foo', 'bar']

INVALID_INIT_TYPES = [ARRAY_XY,
                      DF_XY,
                      DF_INVALID_COLUMNS]


#%% Shapes

SHAPE = [3, 3]

WILDCARD_SHAPES = [(None, SHAPE[1]),
                   (SHAPE[0], None),
                   (None, None)]

WRONG_SHAPE = [i + 1 for i in SHAPE]

WRONG_SHAPES = [(None, WRONG_SHAPE[1]),
                (WRONG_SHAPE[0], None),
                SHAPE[:1],
                SHAPE + [None],
                SHAPE + [0],
                SHAPE + [1],
                SHAPE + [2]]


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


#%% Derivatives

VELOCITY = numpy.array([numpy.nan, 2.5, 5.])

ACCELERATION = numpy.array([numpy.nan, numpy.nan, 1.25])
