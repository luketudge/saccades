# -*- coding: utf-8 -*-
"""The base class for file readers.
"""


class BaseReader:
    """Read eye gaze data from a text file.
    """

    def __init__(self, file, encoding='utf-8', **kwargs):
        """Additional keyword arguments are passed on to :fun:`open`.
        """

        self.file = open(file, mode='r', encoding=encoding, **kwargs)
