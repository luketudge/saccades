# -*- coding: utf-8 -*-

import os

import numpy
import pandas


#%% Paths

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_PATH, 'data')
IMAGES_PATH = os.path.join(BASE_PATH, 'images')


#%% Helper functions

# An arbitrary function, used in test_detect_saccades().
def fun(x, val=True):

    return numpy.full(len(x), val)


# Checks equality of an image file with its reference file.
def image_file_ok(filename):

    img_bytes = open(filename, mode='rb').read()

    reference_filename = os.path.basename(filename)
    reference_path = os.path.join(IMAGES_PATH, 'refs', reference_filename)
    reference_bytes = open(reference_path, mode='rb').read()

    return img_bytes == reference_bytes


#%% Expected contents of top module

MODULE_CONTENTS = ['GazeData',
                   'Saccade',
                   'conversions',
                   'geometry',
                   'saccadedetection',
                   'saccademetrics']


#%% Valid init types

# These are used for parametrization in conftest.py.

SEQUENCE = [[2., 1., 0.],
            [4., 4., 4.],
            [6., 10., 12.]]

ARRAY = numpy.array(SEQUENCE)

DF = pandas.DataFrame(ARRAY,
                      columns=('time', 'x', 'y'),
                      copy=True)

DF_REINDEXED = DF.set_index(numpy.array([9000, 9001, 9002]))

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
                    DF_REINDEXED,
                    DF_CORRECT_SHAPE,
                    DF_EXTRA_COLUMN,
                    DF_REORDERED_COLUMNS]

VALID_INIT_TYPE_NAMES = ['seq',
                         'arr',
                         'df',
                         'df_non_zero_based_index',
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

INVALID_INIT_TYPE_NAMES = ['arr_xy',
                           'df_xy',
                           'df_invalid_cols']


#%% Attributes

SCREEN_RES = [4., 3.]
SCREEN_DIAG = 10.
VIEWING_DIST = 5.
TARGET = [6., 10.]

ATTRIBUTES = {'time_units': None,
              'space_units': 'px',
              'target': TARGET}

SCREEN_ATTRIBUTES = {'screen_res': SCREEN_RES,
                     'screen_diag': SCREEN_DIAG,
                     'viewing_dist': VIEWING_DIST}

ATTRIBUTES.update(SCREEN_ATTRIBUTES)


#%% Shapes

SHAPE = [3, 3]

WILDCARD_SHAPES = [[None, SHAPE[1]],
                   [SHAPE[0], None],
                   [None, None]]

WRONG_SHAPE = [i + 1 for i in SHAPE]

WRONG_SHAPES = [[None, WRONG_SHAPE[1]],
                [WRONG_SHAPE[0], None],
                SHAPE[:1],
                SHAPE + [None],
                SHAPE + [0],
                SHAPE + [1],
                SHAPE + [2]]


#%% Transformations

ORIGIN = [1., 2.]

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


#%% Conversions

# Obviously not realistic that someone sits 2.5 pixels from the screen.
# But it makes the math a bit easier.
VIEWING_DIST_PX = 2.5

# The two easiest angles to check.
PX = [2.5, 0.]
DVA = [45., 0.]


#%% Derivatives

VELOCITY = numpy.array([numpy.nan, 2.5, 5.])
VELOCITY_DVA = numpy.array([numpy.nan, 45., 63.43494882292201])

ACCELERATION = numpy.array([numpy.nan, numpy.nan, 1.25])
ACCELERATION_DVA = numpy.array([numpy.nan, numpy.nan, 9.217474411461005])


#%% Saccade detection

VELOCITY_LOW = 40.
VELOCITY_HIGH = 50.

ACCELERATION_LOW = 5.
ACCELERATION_HIGH = 10.

# The 'exp' key is popped before passing to criterion(),
# and is used to check for the expected result.
CRITERIA = [{'velocity': VELOCITY_LOW, 'exp': [False, True, True]},
            {'velocity': VELOCITY_HIGH, 'exp': [False, False, True]},
            {'acceleration': ACCELERATION_LOW, 'exp': [False, False, True]},
            {'acceleration': ACCELERATION_HIGH, 'exp': [False, False, False]},
            {'velocity': VELOCITY_LOW, 'acceleration': ACCELERATION_LOW, 'exp': [False, False, True]},
            {'velocity': VELOCITY_LOW, 'acceleration': ACCELERATION_HIGH, 'exp': [False, False, False]},
            {'exp': [True, True, True]}]


#%% Saccade

SACCADE = [[2., 1., 2.],
           [4., 5., 5.],
           [6., 9., 8.],
           [8., 7., 10.]]


#%% Saccade metrics

LATENCY = 2.
AMPLITUDE = 10.
AMPLITUDE_DVA = 75.96375653207353


#%% Plotting

# Plotting saccades is tested in test_script.py
# because the simple test data used here are too short for a saccade.

IMAGE_FORMAT = '.png'

PLOT_ARGS = [{'filename': 'test_plot'},
             {'filename': 'test_plot_reverse_y', 'reverse_y': True},
             {'filename': 'test_plot_raw_data', 'show_raw': True},
             {'filename': 'test_plot_saccades', 'saccades': True}]

PLOT_ARGS_NAMES = [x['filename'] for x in PLOT_ARGS]

for x in PLOT_ARGS:
    x['filename'] = os.path.join(IMAGES_PATH, x['filename'] + IMAGE_FORMAT)
