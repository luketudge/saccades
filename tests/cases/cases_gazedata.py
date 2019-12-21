# -*- coding: utf-8 -*-
"""Test cases for gaze data.
"""

import numpy
import pandas


# %% Init data

# Use a numpy array as canonical data format.
# This makes comparisons easy with numpy.array_equal().

data = numpy.array([[0., 1., 2.],
                    [2., 3., 4.],
                    [4., 5., 6.],
                    [6., 7., 8.]])

# Make some variations on pandas DataFrames,
# since this is likely to be a common input type.

colnames = ['time', 'x', 'y']

data_df = pandas.DataFrame(data, columns=colnames, copy=True)

indices = numpy.array(range(9000, 9000 + data.shape[0]))
data_df_reindexed = data_df.set_index(indices)

data_df_shape_only = data_df.copy()
data_df_shape_only.columns = ['a', 'b', 'c']

data_df_extra_col = data_df.copy()
data_df_extra_col['foo'] = 'foo'

data_df_reordered = data_df_extra_col.copy()
data_df_reordered = data_df_reordered[['foo', 'y', 'time', 'x']]

GAZE_DATA = {
    'list': {
        'in': {'data': data.tolist()},
        'out': {}
    },
    'dict': {
        'in': {'data': {col: list(data[:, i]) for i, col in enumerate(colnames)}},
        'out': {}
    },
    'array': {
        'in': {'data': data},
        'out': {}
    },
    'dataframe': {
        'in': {'data': data_df},
        'out': {}
    },
    'dataframe_unnamed': {
        'in': {'data': pandas.DataFrame(data, copy=True)},
        'out': {}
    },
    'dataframe_shape_only': {
        'in': {'data': data_df_shape_only},
        'out': {}
    },
    'dataframe_reindexed': {
        'in': {'data': data_df_reindexed},
        'out': {}
    },
    'dataframe_extra_col': {
        'in': {'data': data_df_extra_col},
        'out': {'columns': ['foo']}
    },
    'dataframe_reordered': {
        'in': {'data': data_df_reordered},
        'out': {'columns': ['foo']}
    },
}

# Add the expected column names.

for case in GAZE_DATA:
    if 'columns' in GAZE_DATA[case]['out']:
        GAZE_DATA[case]['out']['columns'].extend(colnames)
    else:
        GAZE_DATA[case]['out']['columns'] = colnames

# Add the expected output data.

for case in GAZE_DATA:
    GAZE_DATA[case]['out']['data'] = data


# %% Invalid init data

data_xy = data[:, 1:3].copy()

data_df_invalid_cols = data_df_extra_col.copy()
data_df_invalid_cols.columns = ['foo', 'x', 'y', 'bar']

INVALID_GAZE_DATA = {
    'array_xy_only': {
        'in': {'data': data_xy},
        'out': {}
    },
    'dataframe_xy_only': {
        'in': {'data': pandas.DataFrame(data_xy, columns=['x', 'y'], copy=True)},
        'out': {}
    },
    'dataframe_invalid_cols': {
        'in': {'data': data_df_invalid_cols},
        'out': {}
    },
}

# Add the expected exception.

for case in INVALID_GAZE_DATA:
    INVALID_GAZE_DATA[case]['out']['exception'] = ValueError


# %% Attributes

# Define the default attributes

default_attrs = {'time_units': None,
                 'space_units': None,
                 'screen_res': None,
                 'screen_diag': None,
                 'viewing_dist': None,
                 'target': None,
                 'messages': None}

ATTRIBUTES = {
    'dummy': {
        'in': {'attrs': {attr: 'foo' for attr in default_attrs}},
        'out': {}
    },
}

# Add the expected output attributes.
# These are the same as those that went in,
# but just in case this changes later.

for case in ATTRIBUTES:
    ATTRIBUTES[case]['out']['attrs'] = ATTRIBUTES[case]['in']['attrs']
