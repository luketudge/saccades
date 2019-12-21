# -*- coding: utf-8 -*-
"""Test cases for gaze data.
"""

import numpy
import pandas


# %% Input data

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
        'in':
            {'data': data.tolist()},
    },
    'dict': {
        'in':
            {'data': {col: list(data[:, i]) for i, col in enumerate(colnames)}},
    },
    'array': {
        'in':
            {'data': data},
    },
    'dataframe': {
        'in':
            {'data': data_df},
    },
    'dataframe_unnamed': {
        'in':
            {'data': pandas.DataFrame(data)},
    },
    'dataframe_reindexed': {
        'in':
            {'data': data_df_reindexed},
    },
    'dataframe_shape_only': {
        'in':
            {'data': data_df_shape_only},
    },
    'dataframe_extra_col': {
        'in':
            {'data': data_df_extra_col},
    },
    'dataframe_reordered': {
        'in':
            {'data': data_df_reordered},
    },
}

# Add the expected output.

for case in GAZE_DATA:
    GAZE_DATA[case]['out'] = {'data': data}
