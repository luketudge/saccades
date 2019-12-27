# -*- coding: utf-8 -*-
"""Test cases for gaze data.
"""

import functools
import os

import numpy
import pandas

from .. import DATA_PATH
from .. import TEMP_PATH
from .. import REFS_PATH

from saccades import GazeData


# %% Setup wrapped GazeData methods

# Used in testing some other methods,
# and in testing plot().

center = functools.partial(GazeData.center, origin=[1., 1.])
rotate = functools.partial(GazeData.rotate, theta=numpy.pi)


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

colmeans = [3., 4., 5.]

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
    GAZE_DATA[case]['out']['colmeans'] = colmeans


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


# %% Indexing

all_cols = ['time', 'x', 'y']

INDEX = {
    'rows': {
        'in': {'data': data, 'rows': slice(2), 'cols': all_cols},
        'out': {'data': data[:2, :], 'valid': True},
    },
    'rows_boolean': {
        'in': {'data': data, 'rows': data[:, 0] < 3, 'cols': all_cols},
        'out': {'data': data[:2, :], 'valid': True},
    },
    'complete_cols': {
        'in': {'data': data, 'rows': slice(None), 'cols': all_cols},
        'out': {'data': data, 'valid': True},
    },
    'incomplete_cols': {
        'in': {'data': data, 'rows': slice(None), 'cols': ['x', 'y']},
        'out': {'data': data[:, 1:3], 'valid': False},
    },
}


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


# %% NA values

data_nans = data.copy()
data_nans[0, 1:3] = numpy.nan

NANS = {
    'no_nans': {
        'in': {'data': data, 'subset': None},
        'out': {'data': data}
    },
    'nans': {
        'in': {'data': data_nans, 'subset': None},
        'out': {'data': data[1:, :]}
    },
    'nans_in_subset': {
        'in': {'data': data_nans, 'subset': ['x', 'y']},
        'out': {'data': data[1:, :]}
    },
    'nans_not_in_subset': {
        'in': {'data': data_nans, 'subset': ['time']},
        'out': {'data': data_nans}
    },
}


# %% Methods

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


# %% Plotting

plot_data = pandas.read_csv(os.path.join(DATA_PATH, 'comma_delimited.csv'),
                            names=('time', 'x', 'y'))

plot_data_saccade = plot_data.copy()
plot_data_saccade['saccade'] = False
plot_data_saccade.loc[97:111, 'saccade'] = True

PLOT = {
    'default': {
        'in': {
            'data': plot_data,
            'transform': [],
            'format': 'png',
            'kwargs': {}},
        'out': {}
    },
    'reversed': {
        'in': {
            'data': plot_data,
            'transform': [],
            'format': 'png',
            'kwargs': {'reverse_y': True}},
        'out': {}
    },
    'centered': {
        'in': {
            'data': plot_data,
            'transform': [center],
            'format': 'png',
            'kwargs': {'show_raw': True}},
        'out': {}
    },
    'rotated': {
        'in': {
            'data': plot_data,
            'transform': [rotate],
            'format': 'png',
            'kwargs': {'show_raw': True}},
        'out': {}
    },
    'saccades': {
        'in': {
            'data': plot_data_saccade,
            'transform': [],
            'format': 'png',
            'kwargs': {'saccades': True}},
        'out': {}
    },
    'no_saccades': {
        'in': {
            'data': plot_data,
            'transform': [],
            'format': 'png',
            'kwargs': {'saccades': True}},
        'out': {}
    },
    'all_options': {
        'in': {
            'data': plot_data_saccade,
            'transform': [center, rotate],
            'format': 'png',
            'kwargs': {'reverse_y': True, 'show_raw': True, 'saccades': True}},
        'out': {}
    },
}

# Expand the file name to a full path.
# Add the path to the reference file.

for case in PLOT:
    filename = case + '.' + PLOT[case]['in']['format']
    PLOT[case]['in']['filepath'] = os.path.join(TEMP_PATH, filename)
    PLOT[case]['out']['filepath'] = os.path.join(REFS_PATH, filename)
