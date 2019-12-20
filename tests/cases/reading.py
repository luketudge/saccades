# -*- coding: utf-8 -*-
"""Test cases for reading text data files.
"""

import copy
import os

import numpy
import pandas
import regex

from .. import DATA_PATH
from .. import helpers

from saccades.readers import BaseReader as Reader
from saccades.readers import regexes


# %% A custom reader subclass

# This is used as the reader for the preprocessed data file,
# which has a somewhat atypical format.
# This serves as a test of subclassing the basic Reader class.

class NewReader(Reader):

    # The data row pattern for this file is:
    # POS_INTEGER NUMBER NUMBER FILLER
    # So we override the corresponding method.
    def build_row_pattern(self):

        row_groups = ['(?P<time>{})', '(?P<x>{})', '(?P<y>{})']
        row_groups = self.sep.join(row_groups)

        pattern = row_groups.format(regexes.POS_INTEGER,
                                    regexes.NUMBER,
                                    regexes.NUMBER)

        return pattern + regexes.FILLER

    # The final two lines of the header give information
    # about the viewing distance and screen dimensions.
    # So we override the appropriate method for this too.
    def process_header(self, header):

        final_rows = ' '.join(header.splitlines()[-2:])

        pattern = 'gaze ({}) ({})'.format(regexes.POS_INTEGER, regexes.POS_INTEGER)
        match = regex.search(pattern, final_rows)
        screen_res = [float(match.group(i)) for i in range(1, 3)]

        info = {}

        for item in ['distance', 'width', 'height']:
            pattern = '{} ({})'.format(item, regexes.FLOAT)
            match = regex.search(pattern, final_rows)
            info[item] = float(match.group(1))

        screen_diag = numpy.linalg.norm([info['width'], info['height']])

        screen_info = {'screen_res': screen_res,
                       'screen_diag': screen_diag,
                       'viewing_dist': info['distance']}

        return screen_info

    # And we would like to put the header information into each block.
    # So finally we override the method for this.
    def process_data(self, data, messages):

        gd = super().process_data(data, messages)

        gd.screen_res = self.header['screen_res']
        gd.screen_diag = self.header['screen_diag']
        gd.viewing_dist = self.header['viewing_dist']

        return gd


# %% Data files

DATA_FILES = {
    'empty': {
        'in': {
            'file': 'empty.txt',
            'reader': Reader,
            },
        'out': {
            'header': '',
            'n_blocks': 0,
        }
    },
    'csv': {
        'in': {
            'file': 'comma_delimited.csv',
            'reader': Reader,
            'sep': ',',
        },
        'out': {
            'header': '',
            'n_blocks': 1,
        }
    },
    'tsv': {
        'in': {
            'file': 'tab_delimited.csv',
            'reader': Reader,
        },
        'out': {
            'header': '',
            'n_blocks': 1,
        }
    },
    'iView': {
        'in': {
            'file': 'iView.txt',
            'reader': Reader,
        },
        'out': {
            'header_rows': 47,
        }
    },
    'eyelink': {
        'in': {
            'file': 'eyelink.txt',
            'reader': Reader,
        },
        'out': {
            'header_rows': 52,
        }
    },
    'eyelink_events': {
        'in': {
            'file': 'eyelink_events.txt',
            'reader': Reader,
        },
        'out': {
            'header_rows': 16,
        }
    }
}

# Add the expected header for the bigger files.

for case in ['iView', 'eyelink', 'eyelink_events']:
    file = DATA_FILES[case]['in']['file']
    n = DATA_FILES[case]['out']['header_rows']
    header = helpers.get_header(os.path.join(DATA_PATH, file), n)
    DATA_FILES[case]['out']['header'] = header

# Add the custom format one.
# Here we expect the header to be processed into a dictionary.

DATA_FILES['custom_format'] = {
    'in': {
        'file': 'preprocessed.txt',
        'reader': NewReader,
    },
    'out': {
        'header': {
            'screen_res': [576., 304.],
            'screen_diag': 0.5370576070786075,
            'viewing_dist': 0.753,
            },
        'n_blocks': 1,
    }
}


# %% Data rows

values = ['0', '1', '2']
colnames = ['time', 'x', 'y']
columns = {col: val for col, val in zip(colnames, values)}

ROW_FORMATS = {
    'standard': {
        'in': {'row': '{time} {x}.0 {y}.0'},
        'out': {'valid': True}
    },
    'no_decimals': {
        'in': {'row': '{time} {x}. {y}.'},
        'out': {'valid': True}
    },
    'negative_xy': {
        'in': {'row': '{time} -{x}.0 -{y}.0'},
        'out': {'valid': True}
    },
    'extra_cols': {
        'in': {'row': '{time} {x}.0 {y}.0 3.0 4.0'},
        'out': {'valid': True}
    },
    'intervening_cols': {
        'in': {'row': '{time} SMP 1 {x}.0 {y}.0'},
        'out': {'valid': True}
    },
    'trailing_separators': {
        'in': {'row': '{time} {x}.0 {y}.0  '},
        'out': {'valid': True}
    },
    'tab_separators': {
        'in': {'row': '{time}\t{x}.0\t{y}.0'},
        'out': {'valid': True}
    },
    'no_time': {
        'in': {'row': '{x}.0 {y}.0'},
        'out': {'valid': False}
    },
    'no_y': {
        'in': {'row': '{time} {x}.0'},
        'out': {'valid': False}
    },
    'float_time': {
        'in': {'row': '{time}.0 {x}.0 {y}.0'},
        'out': {'valid': False}
    },
    'negative_time': {
        'in': {'row': '-{time} {x}.0 {y}.0'},
        'out': {'valid': False}
    },
    'leading_text_time': {
        'in': {'row': 'a{time} {x}.0 {y}.0'},
        'out': {'valid': False}
    },
    'trailing_text_time': {
        'in': {'row': '{time}a {x}.0 {y}.0'},
        'out': {'valid': False}
    },
    'leading_text_xy': {
        'in': {'row': '{time} a{x}.0 a{y}.0'},
        'out': {'valid': False}
    },
    'trailing_text_xy': {
        'in': {'row': '{time} {x}.0a {y}.0a'},
        'out': {'valid': False}
    },
    'cols_between_xy': {
        'in': {'row': '{time} {x}.0 blah {y}.0'},
        'out': {'valid': False}
    },
    'wrong_separator': {
        'in': {'row': '{time};{x}.0;{y}.0'},
        'out': {'valid': False}
    },
}

# Add in the values.

for case in ROW_FORMATS:
    row = ROW_FORMATS[case]['in']['row'].format(**columns)
    ROW_FORMATS[case]['in']['row'] = row
    if ROW_FORMATS[case]['out']['valid']:
        ROW_FORMATS[case]['out']['values'] = [float(val) for val in values]
    else:
        ROW_FORMATS[case]['out']['values'] = None


# %% Data blocks

# Used to test the process_data() method of readers.

# The test data have only two rows,
# so a maximum of two NaN values are possible.

data = {'time': ['2', '4'],
        'x': ['1.', '3.'],
        'y': ['3.', '4.']}

DATA_BLOCKS = {
    'standard': {
        'in': {'nan_values': None}
    },
    'no_nan_values': {
        'in': {'nan_values': []}
    },
    'float_zero_nan': {
        'in': {'nan_values': ['0.0']}
    },
}

# Add in the dictionaries of string data values,
# and insert NaN values as necessary.
# If no nan values are requested,
# insert one instance of the default NaN value '.'

for case in DATA_BLOCKS:

    data_in = copy.deepcopy(data)
    data_out = pandas.DataFrame(data).astype(float)
    nan_values = DATA_BLOCKS[case]['in']['nan_values']

    if nan_values is None:
        data_in['x'][0] = '.'
        data_out.loc[0, 'x'] = numpy.nan
    else:
        for row, val in enumerate(nan_values):
            data_in['x'][row] = val
            data_out.loc[row, 'x'] = numpy.nan

    DATA_BLOCKS[case]['in']['data'] = data_in
    DATA_BLOCKS[case]['out'] = {'data': data_out}
