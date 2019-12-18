#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This file doubles as an example script and a minimal functional test \
to check only that no exceptions occur during basic use.
"""

import os
import webbrowser

from saccades.readers import BaseReader
from saccades.readers.regexes import FILLER
from saccades.readers.regexes import POS_INTEGER
from saccades.readers.regexes import NUMBER


# %% Setup

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

DATA_FILENAME = 's1_actioncliptest00001.txt'
DATA_PATH = os.path.join(BASE_PATH, 'data', DATA_FILENAME)

IMAGE_FILENAME = 'example_plot.png'
IMAGE_PATH = os.path.join(BASE_PATH, IMAGE_FILENAME)


# %% Subclass of BaseReader

class NewReader(BaseReader):

    # The data row pattern for this file is:
    # POS_INTEGER NUMBER NUMBER FILLER
    # So we override the corresponding method.
    def build_row_pattern(self):

        row_groups = ['(?P<time>{})', '(?P<x>{})', '(?P<y>{})']
        row_groups = self.sep.join(row_groups)

        return row_groups.format(POS_INTEGER, NUMBER, NUMBER) + FILLER


# %% Test function

def test_script():

    # Load the data using the new reader.
    f = NewReader(DATA_PATH)

    # Check the header.
    print(f.header)

    # Get the blocks of data.
    blocks = list(f.get_blocks())
    print('{} blocks loaded'.format(len(blocks)))

    # Get the first block.
    gd = blocks[0]
    print(gd)

    # Save a plot.
    gd.plot(filename=IMAGE_PATH)


# %% Script mode

if __name__ == '__main__':

    test_script()
    webbrowser.open(IMAGE_PATH)
