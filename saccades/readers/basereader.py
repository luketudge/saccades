# -*- coding: utf-8 -*-
"""The base class for file readers.
"""

import numpy
import pandas
import regex

from .. import GazeData
from ..gazedata import INIT_COLUMNS
from .regexes import FILLER
from .regexes import FLAGS
from .regexes import FLOAT
from .regexes import POS_INTEGER


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

    def __init__(self, file, sep=r'\s+', na_values=['.', '-.'], encoding='utf-8', **kwargs):
        """File is always opened in read-only mode.

        Additional keyword arguments are passed on to :func:`open`.

        :param file: Path to a file containing gaze data.
        :type file: str
        :param sep: Column separator for rows of gaze data.
        :type sep: str
        :param na_values: Values to replace with `numpy.nan` \
        if present in a data row.
        :type na_values: sequence
        """

        self.filename = file
        self.sep = sep
        self.na_values = na_values
        self.encoding = encoding
        self.open_kwargs = kwargs

        self.row_pattern = regex.compile(self.build_row_pattern(), flags=FLAGS)
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
        :rtype: str
        """

        intervening_columns = self.sep.join(['(', '|', FILLER, ')'])
        row_end = '($|{}{})'.format(self.sep, FILLER)
        row_groups = '(?P<{}>{}){}(?P<{}>{}){}(?P<{}>{}){}'
        row = row_groups.format(INIT_COLUMNS[0], POS_INTEGER,
                                intervening_columns,
                                INIT_COLUMNS[1], FLOAT,
                                self.sep,
                                INIT_COLUMNS[2], FLOAT,
                                row_end)

        return row

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
        """Process data together with accompanying messages.

        This method ensures the essential columns are numeric, \
        converts to :class:`GazeData`, \
        and adds the messages to the *messages* attribute \
        after processing with :meth:`process_messages`.

        Override this method in subclasses, \
        calling ``super().process_data()`` \
        to add these final steps.

        :return: Modified data.
        :rtype: :class:`GazeData`
        """

        data = GazeData(data.astype({col: float for col in INIT_COLUMNS}))

        data.messages = self.process_messages(messages)

        return data

    def get_blocks(self, cols=INIT_COLUMNS):
        """Get blocks of gaze data from the file.

        A block is a group of consecutive rows of data \
        without intervening non-data lines. \
        The occurrence of a non-data line \
        marks the start of a new block.

        Blocks are instances of :class:`pandas.DataFrame`, \
        and are passed on to :meth:`process_data`, \
        together with any text messages preceding the block.

        :param cols: Columns to include.
        :type cols: sequence
        :return: Successive blocks of data.
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
                        val = match.group(col)
                        if val in self.na_values:
                            val = numpy.nan
                        data_buffer[col].append(val)

                    getting_data = True

                # We have a message.
                else:

                    # But we were getting data,
                    # so that means we are at the end of a block.
                    if getting_data:

                        messages = ''.join(message_buffer).rstrip('\n')

                        yield self.process_data(pandas.DataFrame(data_buffer), messages)

                        message_buffer = []
                        data_buffer = {col: [] for col in cols}
                        getting_data = False

                    message_buffer.append(line)

        # We still have some data in the buffer at the end,
        # so we put together the final block.
        if message_buffer or data_buffer[cols[0]]:

            messages = ''.join(message_buffer).rstrip('\n')

            yield self.process_data(pandas.DataFrame(data_buffer), messages)
