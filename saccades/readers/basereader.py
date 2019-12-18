# -*- coding: utf-8 -*-
"""The base class for file readers.
"""

import regex

from .. import GazeData


# %% Regular expressions

FLAGS = regex.V1

# 1 or more digits.
INTEGER = r'\d+'

# 0 or more digits, then a dot, then 0 or more digits.
FLOAT = r'\d*\.\d*'

# INTEGER or FLOAT.
NUMBER = '({}|{})'.format(INTEGER, FLOAT)

# 0 or more occurrences of any character.
FILLER = '.*'


# %% Main class

class BaseReader:
    """Read eye gaze data from a text file.

    This base class just finds the coordinate gaze data \
    and reads in all other contents as unprocessed strings.

    Subclasses will mainly need to override the following methods:

    * :meth:`build_row_pattern` \
    to construct a custom regular expression for a row of data.
    * :meth:`process_header` \
    to turn the raw text file header into something else.
    * :meth:`process_messages` \
    to turn raw text message lines into something else.
    * :meth:`process_data` \
    to modify gaze data according to any preceding messages.
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
        self.header = self.process_header(self.get_header())

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

        :return: Regular expression matching a row of data.
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

        :return: Header content.
        :rtype: str
        """

        header_lines = []

        with self:

            for line in self.file:
                if self.row_pattern.fullmatch(line.rstrip('\n')):
                    break
                header_lines.append(line)

        return ''.join(header_lines).rstrip('\n')

    def process_header(self, header):
        """Process a raw text header.

        Override this method in subclasses.

        :return: Unprocessed header.
        """

        return header

    def process_messages(self, messages):
        """Process raw text message lines.

        Override this method in subclasses.

        :return: Unprocessed messages.
        """

        return messages

    def process_data(self, data, messages):
        """Process gaze data together with accompanying messages.

        This method just adds the raw messages \
        to the *messages* attribute of the data.

        Override this method in subclasses.

        :return: Modified data.
        :rtype: :class:`GazeData`
        """

        data.messages = messages

        return data

    def get_blocks(self, cols=['time', 'x', 'y']):
        """Get blocks of gaze data from the file.

        A block is a group of consecutive rows of data \
        without intervening non-data lines. \
        The occurrence of a non-data line \
        marks the start of a new block.

        Blocks are instances of :class:`GazeData`. \
        Any non-data lines preceding the block \
        are placed in the *messages* attribute, \
        after processing with :meth:`process_messages`.

        :param cols: Columns to include.
        :type cols: sequence
        :return: Successive instances of :class:`GazeData`.
        :rtype: :class:`generator`
        """

        message_buffer = []
        data_buffer = {col: [] for col in cols}
        getting_data = False

        with self:

            for line in self.file:

                match = self.row_pattern.fullmatch(line.rstrip('\n'))

                # We have a row of data.
                if match:
                    for col in cols:
                        data_buffer[col].append(match.group(col))
                    getting_data = True

                # We have a message.
                else:

                    # But we were getting data,
                    # so that means we are at the end of a block.
                    if getting_data:

                        messages = ''.join(message_buffer).rstrip('\n')
                        messages = self.process_messages(messages)

                        yield self.process_data(GazeData(data_buffer), messages)

                        message_buffer = []
                        data_buffer = {col: [] for col in cols}
                        getting_data = False

                    message_buffer.append(line)
