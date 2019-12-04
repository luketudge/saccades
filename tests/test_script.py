#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This file doubles as a functional test, \
which tests basic use of the saccades package \
and checks only that no exceptions occur, \
and an example script demonstrating basic use.
"""

import os

import pandas

import saccades


#%% Setup

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
FILENAME = 'example.csv'
FILE_PATH = os.path.join(BASE_PATH, 'data', FILENAME)

DF = pandas.read_csv(FILE_PATH, header=None)


def test_script():

    ## Turn a pandas DataFrame into GazeData.
    gd = saccades.GazeData(DF)

    ## Calculate velocity and acceleration.
    gd.get_accelerations()

    ## Display the data.
    print(gd)
