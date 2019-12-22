# -*- coding: utf-8 -*-
"""Test cases for gaze data.
"""

import functools

import numpy
import pandas

from saccades import GazeData


# %% Helper functions

def mark_all(x, val=True):
    """A dummy function for event detection.

    Marks every sample as an event (or non-event if val=False).
    """

    return numpy.full(len(x), val)


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
    'array': {
        'in': {'data': data},
        'out': {}
    },
    'list': {
        'in': {'data': data.tolist()},
        'out': {}
    },
    'dict': {
        'in': {'data': {col: list(data[:, i]) for i, col in enumerate(colnames)}},
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

gazedata_attributes = ['time_units',
                       'space_units',
                       'target',
                       'messages']

screen_info = ['screen_res',
               'screen_diag',
               'viewing_dist']

empty_attrs = {key: None for key in gazedata_attributes + screen_info}

valid_screen_info = empty_attrs.copy()
valid_screen_info.update({'screen_res': [1366., 768.],
                          'screen_diag': 12.,
                          'viewing_dist': 9000.})

ATTRIBUTES = {
    'empty': {
        'in': {'attrs': empty_attrs},
        'out': {'valid': False}
    },
    'dummy': {
        'in': {'attrs': {attr: 'foo' for attr in empty_attrs}},
        'out': {'valid': True}
    },
    'valid_screen_info': {
        'in': {'attrs': valid_screen_info},
        'out': {'valid': True}
    },
}

# Add some cases that are missing one of the screen attributes.

for attr in screen_info:
    id = 'missing_' + attr
    attrs_dict = valid_screen_info.copy()
    attrs_dict[attr] = None
    data_in = {'attrs': attrs_dict}
    data_out = {'valid': False, 'error_msg': attr}
    ATTRIBUTES[id] = {'in': data_in, 'out': data_out}

# Add the expected output attributes.
# These are the same as those that went in.

for case in ATTRIBUTES:
    ATTRIBUTES[case]['out']['attrs'] = ATTRIBUTES[case]['in']['attrs']

# Add the expected exception if needed.

for case in ATTRIBUTES:
    if not ATTRIBUTES[case]['out']['valid']:
        ATTRIBUTES[case]['out']['exception'] = AttributeError
        if 'error_msg' not in ATTRIBUTES[case]['out']:
            ATTRIBUTES[case]['out']['error_msg'] = 'necessary attributes have not yet been set'


# %% Methods

center = functools.partial(GazeData.center, origin=[-9000., -9000.])
rotate = functools.partial(GazeData.rotate, theta=numpy.pi)

METHODS = {
    'reset_time': {
        'in': {'method': GazeData.reset_time},
        'out': {'saves_coords': False}
    },
    'center': {
        'in': {'method': center},
        'out': {'saves_coords': True}
    },
    'rotate': {
        'in': {'method': rotate},
        'out': {'saves_coords': True}
    },
}


# %% Saccade detection

no_saccades = functools.partial(mark_all, val=False)
one_saccade = functools.partial(mark_all, val=True)

DETECTION = {
    'no_hits': {
        'in': {'func': no_saccades, 'n': None, 'kwargs': {}},
        'out': {'n': 0, 'column': False}
    },
    'no_hits_lots_requested': {
        'in': {'func': no_saccades, 'n': 9000, 'kwargs': {}},
        'out': {'n': 0, 'column': False}
    },
    'one_hit': {
        'in': {'func': one_saccade, 'n': None, 'kwargs': {}},
        'out': {'n': 1, 'column': True}
    },
    'one_hit_lots_requested': {
        'in': {'func': one_saccade, 'n': 9000, 'kwargs': {}},
        'out': {'n': 1, 'column': True}
    },
    'one_hit_zero_requested': {
        'in': {'func': one_saccade, 'n': 0, 'kwargs': {}},
        'out': {'n': 0, 'column': True}
    },
    'with_kwargs': {
        'in': {'func': mark_all, 'n': None, 'kwargs': {'val': True}},
        'out': {'n': 1, 'column': True}
    },
    'with_non_default_kwargs': {
        'in': {'func': mark_all, 'n': None, 'kwargs': {'val': False}},
        'out': {'n': 0, 'column': False}
    },
}
