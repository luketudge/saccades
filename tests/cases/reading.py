# -*- coding: utf-8 -*-
"""Test cases for reading text data files.
"""

import copy
import os

import numpy
import pandas
import regex

from .. import DATA_PATH

from saccades.readers import Reader
from saccades.readers import regexes


# %% Helper functions

def get_header(file, n):
    """Get the header section of a text gaze data file.
    """

    header = []

    with open(file, encoding='utf-8') as f:
        for i in range(n):
            header.append(f.readline())

    return ''.join(header).rstrip('\n')


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
            },
        'out': {
            'n_blocks': 0,
        }
    },
    'csv': {
        'in': {
            'file': 'comma_delimited.csv',
            'sep': ',',
        },
        'out': {
            'n_blocks': 1,
        }
    },
    'tsv': {
        'in': {
            'file': 'tab_delimited.tsv',
        },
        'out': {
            'n_blocks': 1,
        }
    },
    'iView': {
        'in': {
            'file': 'iView.txt',
        },
        'out': {
            'header_rows': 47,
        }
    },
    'eyelink': {
        'in': {
            'file': 'eyelink.txt',
        },
        'out': {
            'header_rows': 52,
        }
    },
    'eyelink_events': {
        'in': {
            'file': 'eyelink_events.txt',
        },
        'out': {
            'header_rows': 16,
        }
    },
    'custom_format': {
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
    },
}

# Expand the file name to a full path.

for case in DATA_FILES:
    filepath = os.path.join(DATA_PATH, DATA_FILES[case]['in']['file'])
    DATA_FILES[case]['in']['filepath'] = filepath

# Make a dictionary of keyword arguments for the reader.

for case in DATA_FILES:

    reader_kwargs = {}

    if 'sep' in DATA_FILES[case]['in']:
        reader_kwargs['sep'] = DATA_FILES[case]['in']['sep']

    DATA_FILES[case]['in']['kwargs'] = reader_kwargs

# Add the default reader if none specified.

for case in DATA_FILES:

    if 'reader' not in DATA_FILES[case]['in']:
        DATA_FILES[case]['in']['reader'] = Reader

# Add the expected header if any.

for case in DATA_FILES:

    if 'header_rows' in DATA_FILES[case]['out']:
        file = DATA_FILES[case]['in']['filepath']
        n = DATA_FILES[case]['out']['header_rows']
        header = get_header(file, n)
        DATA_FILES[case]['out']['header'] = header
    elif 'header' not in DATA_FILES[case]['out']:
        DATA_FILES[case]['out']['header'] = ''


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


# %% Data blocks

# Used to test the process_data() method of readers.
# Add more rows to data if more NaN values are needed,
# as we can only test as many different NaN values
# as there are rows in the test data.

data = {'time': ['2', '4'],
        'x': ['1.', '3.'],
        'y': ['3.', '4.']}

DATA_BLOCKS = {
    'standard': {
        'in': {},
        'out': {}
    },
    'no_na_values': {
        'in': {'na_values': []},
        'out': {}
    },
    'zero_is_na': {
        'in': {'na_values': ['0.0']},
        'out': {}
    },
}

# Add in the dictionaries of string data values,
# and insert NaN values as necessary.
# If no NaN values are requested,
# insert one instance of the default NaN value '.'

for case in DATA_BLOCKS:

    data_in = copy.deepcopy(data)
    data_out = pandas.DataFrame(data).astype(float)

    if 'na_values' in DATA_BLOCKS[case]['in']:
        na_values = DATA_BLOCKS[case]['in']['na_values']
        for row, val in enumerate(na_values):
            data_in['x'][row] = val
            data_out.loc[row, 'x'] = numpy.nan
    else:
        data_in['x'][0] = '.'
        data_out.loc[0, 'x'] = numpy.nan

    DATA_BLOCKS[case]['in']['data'] = data_in
    DATA_BLOCKS[case]['out']['data'] = data_out
