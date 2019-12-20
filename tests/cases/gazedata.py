# -*- coding: utf-8 -*-
"""Test cases for gaze data.
"""

import numpy
import pandas


# %% Input data

colnames = ['time', 'x', 'y']

# Use a numpy array as canonical data format.
# This makes comparisons easy with numpy.array_equal().

data = numpy.array([[0., 1., 2.],
                    [2., 3., 4.],
                    [4., 5., 6.]])

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
            {'data': pandas.DataFrame(data, columns=colnames)},
    },
    'dataframe_unnamed': {
        'in':
            {'data': pandas.DataFrame(data)},
    },
}

# Add the expected output.

for case in GAZE_DATA:
    GAZE_DATA[case]['out'] = {'data': data}
