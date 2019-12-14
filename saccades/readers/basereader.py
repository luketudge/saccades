# -*- coding: utf-8 -*-
"""The base class for file readers.
"""

import regex


#%% Regular expressions

DEFAULT_SEPARATOR = '\\s+'


#%% Main class

class BaseReader:
    """Read eye gaze data from a text file.
    """

    def __init__(self, file, sep=DEFAULT_SEPARATOR, encoding='utf-8', **kwargs):
        """File is always opened in read-only mode.

        Additional keyword arguments are passed on to :func:`open`.

        :param file: Path to a file containing gaze data.
        :type file: str
        :param sep: Column separator for rows of gaze data.
        :type sep: str or
        """

        self.file = open(file, mode='r', encoding=encoding, **kwargs)

        self.sep = regex.compile(sep)
