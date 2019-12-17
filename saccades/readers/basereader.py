# -*- coding: utf-8 -*-
"""The base class for file readers.
"""

import regex


# %% Regular expressions

FLAGS = regex.V1

# 1 or more digits.
INTEGER = r'\d+'

# 1 or more digits, then a dot, then 1 or more digits
FLOAT = r'\d+\.\d+'

# 0 or more occurrences of any character.
FILLER = '.*'


# %% Main class

class BaseReader:
    """Read eye gaze data from a text file.

    This base class just finds the coordinate gaze data \
    and reads in all other contents as unprocessed strings.
    """

    def __init__(self, file, sep=r'\s+', encoding='utf-8', **kwargs):
        """File is always opened in read-only mode.

        Additional keyword arguments are passed on to :func:`open`.

        :param file: Path to a file containing gaze data.
        :type file: str
        :param sep: Column separator for rows of gaze data.
        :type sep: str
        """

        intervening_columns = sep.join(['(', '|', FILLER, ')'])
        row_end = '($|{}{})'.format(sep, FILLER)
        row_groups = '(?P<time>{}){}(?P<x>{}){}(?P<y>{}){}'
        row = row_groups.format(INTEGER, intervening_columns, FLOAT, sep, FLOAT, row_end)
        self.row_pattern = regex.compile(row, flags=FLAGS)

        self.filename = file
        self.encoding = encoding
        self.open_kwargs = kwargs

    def __enter__(self):

        self.file = open(self.filename, mode='r',
                         encoding=self.encoding, **self.open_kwargs)

        return self

    def __exit__(self, exc_type, exc_value, traceback):

        self.file.close()
