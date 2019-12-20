# -*- coding: utf-8 -*-
"""Some helper functions used during testing.
"""

import os

import numpy


# %% Functions for data files

def get_header(file, n):
    """Get the header section of a text gaze data file.
    """

    header = []

    with open(file, encoding='utf-8') as f:
        for i in range(n):
            header.append(f.readline())

    return ''.join(header).rstrip('\n')


def files_equal(file1, file2):
    """Determine whether two files have the same content.
    """

    bytes1 = open(file1, mode='rb').read()
    bytes2 = open(file2, mode='rb').read()

    return bytes1 == bytes2


# %% Functions for gaze data

def mark_all(x, val=True):
    """A dummy function for event detection.

    Marks every sample as an event (or non-event if val=False).
    """

    return numpy.full(len(x), val)
