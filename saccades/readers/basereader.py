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

        self.filename = file
        self.sep = sep
        self.encoding = encoding
        self.open_kwargs = kwargs

        self.row_pattern = self.build_row_pattern()
        self.header = self.get_header()

    def __enter__(self):

        self.file = open(self.filename, mode='r',
                         encoding=self.encoding, **self.open_kwargs)

        return self

    def __exit__(self, exc_type, exc_value, traceback):

        self.file.close()

    def build_row_pattern(self):
        """Build a regular expression for a row of data.

        A row of data:

        * contains values separated by the separator \
        specified in :meth:`__init__`
        * begins with an integer value (the *time* column)
        * contains two neighboring float values (the *x* and *y* columns) \
        (the first such pair of values is used if more than one occurs)

        :rtype: :class:`regex.regex.Pattern`
        """

        intervening_columns = self.sep.join(['(', '|', FILLER, ')'])
        row_end = '($|{}{})'.format(self.sep, FILLER)
        row_groups = '(?P<time>{}){}(?P<x>{}){}(?P<y>{}){}'
        row = row_groups.format(INTEGER, intervening_columns, FLOAT,
                                self.sep, FLOAT, row_end)

        return regex.compile(row, flags=FLAGS)

    def get_header(self):
        """Get the header section of the file.

        The header is all the rows up to the first row of data \
        (see :meth:`build_row_pattern`).

        :rtype: str
        """

        header_lines = []

        with self:

            for line in self.file:
                if self.row_pattern.fullmatch(line.rstrip('\n')):
                    break
                header_lines.append(line)

        return ''.join(header_lines).rstrip('\n')
