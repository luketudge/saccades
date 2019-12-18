#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This file doubles as an example script and a minimal functional test \
to check only that no exceptions occur during basic use.
"""

import os
import webbrowser

from saccades.readers import BaseReader


# %% Setup

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

DATA_FILENAME = 'example_eyelink.txt'
DATA_PATH = os.path.join(BASE_PATH, 'data', DATA_FILENAME)

IMAGE_FILENAME = 'example_plot.png'
IMAGE_PATH = os.path.join(BASE_PATH, IMAGE_FILENAME)


# %% Test function

def test_script():

    # Load the data using the new reader.
    f = BaseReader(DATA_PATH)

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
