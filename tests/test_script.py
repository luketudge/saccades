#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This file doubles as an example script demonstrating basic use, \
and a very minimal functional test \
that tests basic use and checks only that no exceptions occur.
"""

import os

import pandas

import saccades


#%% Setup

FILENAME = 'example.csv'
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_PATH, 'data', FILENAME)

CENTER = (320, 240)

DF = pandas.read_csv(FILE_PATH, header=None)


def test_script():

    ## Turn a pandas DataFrame into GazeData.
    gd = saccades.GazeData(DF)

    ## Recenter.
    gd.center(CENTER)

    ## Calculate velocity and acceleration.
    gd.get_accelerations()

    ## Display the data.
    print(gd)

    ## Plot.
    gd.plot()
