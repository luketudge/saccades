# -*- coding: utf-8 -*-

import os

import numpy
import pandas


# %% Paths

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_PATH, 'data')
IMAGES_PATH = os.path.join(BASE_PATH, 'images')


# %% Helper functions

# Gets the header section of a text data file.
def get_header(filename, n):

    header = []

    with open(filename, encoding='utf-8') as f:
        for i in range(n):
            header.append(f.readline())

    return ''.join(header).rstrip('\n')


# Gets the needed init arguments from a dictionary of file information,
# like those defined in DATA_FILES below.
def get_basereader_args(file):

    kwargs = {'file': file['file']}

    if 'sep' in file:
        kwargs['sep'] = file['sep']

    return kwargs


# An arbitrary function, used in test_detect_saccades().
def fun(x, val=True):

    return numpy.full(len(x), val)


# Checks equality of an image file with its reference file.
def image_file_ok(filepath):

    img_bytes = open(filepath, mode='rb').read()

    reference_filename = os.path.basename(filepath)
    reference_path = os.path.join(IMAGES_PATH, 'refs', reference_filename)
    reference_bytes = open(reference_path, mode='rb').read()

    return img_bytes == reference_bytes


# %% Expected contents of modules

MODULE_CONTENTS = ['GazeData',
                   'Saccade',
                   'conversions',
                   'geometry',
                   'detection',
                   'metrics',
                   '__version__']

READERS_CONTENTS = ['BaseReader']


# %% Data files

DATA_FILES = [
    {'filename': 'empty.txt', 'data_start': 0},
    {'filename': 'example.tsv', 'data_start': 0},
    {'filename': 'example.csv', 'data_start': 0, 'sep': ','},
    {'filename': 'example_iView.txt', 'data_start': 47},
    {'filename': 'example_eyelink.txt', 'data_start': 52},
    {'filename': 'example_eyelink_events.txt', 'data_start': 16},
    {'filename': 's1_actioncliptest00001.txt', 'data_start': 11}
]

for f in DATA_FILES:
    f['file'] = os.path.join(DATA_PATH, f['filename'])
    f['header'] = get_header(f['file'], f['data_start'])

DATA_FILE_IDS = [x['filename'] for x in DATA_FILES]


# %% Data rows

VALID_ROWS = [
    '5908926586 SMP 1 275.7813 307.0769 0 1005 0  ',
    '5908926586 SMP 1 275.7813 307.0769 0 1005 0',
    '5908926586 SMP 1 275.7813 307.0769  ',
    '5908926586 SMP 1 275.7813 307.0769 ',
    '5908926586 SMP 1 275.7813 307.0769',
    '5908926586 blah blah blah 275.7813 307.0769',
    '5908926586 SMP 1 275.7813 307.0769 blah blah blah',
    '5908926586 275.7813 307.0769',
    '5908926586\tSMP\t1\t275.7813\t307.0769\t0\t1005\t0\t\t'
]

INVALID_ROWS = [
    'SMP 1 275.7813 307.0769 0 1005 0  ',
    '5908926586 SMP 1 275.7813 ',
    'a5908926586 SMP 1 275.7813 307.0769',
    '5908926586a SMP 1 275.7813 307.0769',
    '5908926586 SMP 1 a275.7813 307.0769 0 1005 0  ',
    '5908926586 SMP 1 275.7813 307.0769a 0 1005 0  ',
    '5908926586,SMP,1,275.7813,307.0769,0,1005,0,,'
]

COLUMN_PATTERNS = [
    '0 1.0 2.0',
    '0 blah 1.0 2.0',
    '0 1.0 2.0 blah',
    '0 1.0 2.0 3.0 4.0',
    '0 1.0 2.0 blah 3.0 4.0',
    '0 1.0 2.0 blah 3.0 4.0 blah'
]


# %% Valid init types

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

STANDARD_INIT_TYPES = {'seq': SEQUENCE,
                       'arr': ARRAY,
                       'df': DF,
                       'df_shape_only': DF_CORRECT_SHAPE}

VALID_INIT_TYPES = {'seq': SEQUENCE,
                    'arr': ARRAY,
                    'df': DF,
                    'df_non_zero_based_index': DF_REINDEXED,
                    'df_shape_only': DF_CORRECT_SHAPE,
                    'df_extra_col': DF_EXTRA_COLUMN,
                    'df_reordered': DF_REORDERED_COLUMNS}


# %% Invalid init types

ARRAY_XY = numpy.array(ARRAY[:, 1:3])

DF_XY = pandas.DataFrame(ARRAY_XY,
                         columns=('x', 'y'),
                         copy=True)

DF_INVALID_COLUMNS = DF_EXTRA_COLUMN.copy()
DF_INVALID_COLUMNS.columns = ['x', 'y', 'foo', 'bar']

INVALID_INIT_TYPES = {'arr_xy': ARRAY_XY,
                      'df_xy': DF_XY,
                      'df_invalid_cols': DF_INVALID_COLUMNS}


# %% Attributes

SCREEN_RES = [4., 3.]
SCREEN_DIAG = 10.
VIEWING_DIST = 5.
TARGET = [6., 10.]

ATTRIBUTES = {'messages': None,
              'time_units': None,
              'space_units': 'px',
              'target': TARGET}

SCREEN_ATTRIBUTES = {'screen_res': SCREEN_RES,
                     'screen_diag': SCREEN_DIAG,
                     'viewing_dist': VIEWING_DIST}

ATTRIBUTES.update(SCREEN_ATTRIBUTES)


# %% Shapes

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


# %% Transformations

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


# %% Conversions

# Obviously not realistic that someone sits 2.5 pixels from the screen.
# But it makes the math a bit easier.
VIEWING_DIST_PX = 2.5

# The two easiest angles to check.
PX = [2.5, 0.]
DVA = [45., 0.]


# %% Derivatives

VELOCITY = numpy.array([numpy.nan, 2.5, 5.])
VELOCITY_DVA = numpy.array([numpy.nan, 45., 63.43494882292201])

ACCELERATION = numpy.array([numpy.nan, numpy.nan, 1.25])
ACCELERATION_DVA = numpy.array([numpy.nan, numpy.nan, 9.217474411461005])


# %% Saccade detection

VELOCITY_LOW = 40.
VELOCITY_HIGH = 50.

ACCELERATION_LOW = 5.
ACCELERATION_HIGH = 10.

# The 'exp' key is popped before passing to criterion(),
# and is used to check for the expected result.
CRITERIA = [
    {'velocity': VELOCITY_LOW, 'exp': [False, True, True]},
    {'velocity': VELOCITY_HIGH, 'exp': [False, False, True]},
    {'acceleration': ACCELERATION_LOW, 'exp': [False, False, True]},
    {'acceleration': ACCELERATION_HIGH, 'exp': [False, False, False]},
    {'velocity': VELOCITY_LOW, 'acceleration': ACCELERATION_LOW, 'exp': [False, False, True]},
    {'velocity': VELOCITY_LOW, 'acceleration': ACCELERATION_HIGH, 'exp': [False, False, False]},
    {'exp': [True, True, True]}
]


# %% Saccade

SACCADE = [[2., 1., 2.],
           [4., 5., 5.],
           [6., 9., 8.],
           [8., 7., 10.]]


# %% Saccade metrics

LATENCY = 2.
DURATION = 6.
AMPLITUDE = 10.
AMPLITUDE_DVA = 75.96375653207353


# %% Plotting

IMAGE_FORMAT = '.png'

PLOT_ARGS = [{'filename': 'test_plot'},
             {'filename': 'test_plot_reverse_y', 'reverse_y': True},
             {'filename': 'test_plot_raw_data', 'show_raw': True},
             {'filename': 'test_plot_saccades', 'saccades': True}]

for x in PLOT_ARGS:
    x['filename'] = os.path.join(IMAGES_PATH, x['filename'] + IMAGE_FORMAT)
