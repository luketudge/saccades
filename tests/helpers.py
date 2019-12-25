# -*- coding: utf-8 -*-
"""Some helper functions used in more than one test module.
"""

from saccades import GazeData
from saccades import Saccade


# %% Init functions

def init_gazedata(data, **kwargs):
    """Initialize a GazeData table from a gaze data test case,
    with additional keyword arguments if necessary.
    """

    return GazeData(data['in']['data'], **kwargs)


def init_saccade(data, **kwargs):
    """Initialize a Saccade table from a gaze data test case,
    with additional keyword arguments if necessary.
    """

    return Saccade(data['in']['data'], **kwargs)


# %% Misc

def files_equal(file1, file2):
    """Determine whether two files have the same content.
    """

    bytes1 = open(file1, mode='rb').read()
    bytes2 = open(file2, mode='rb').read()

    return bytes1 == bytes2
