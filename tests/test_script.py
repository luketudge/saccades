#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This file doubles as an example script demonstrating basic use, \
and a very minimal functional test that tests basic use \
and checks only that no exceptions occur.
"""

import os
import webbrowser

import pandas

import saccades


#%% Setup

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

DATA_FILENAME = 'example.csv'
DATA_PATH = os.path.join(BASE_PATH, 'data', DATA_FILENAME)

DF = pandas.read_csv(DATA_PATH, header=None)

CENTER = (320, 240)

IMAGE_FILENAME = 'test_script.png'
IMAGE_PATH = os.path.join(BASE_PATH, 'images', IMAGE_FILENAME)


#%% Test function

def test_script():

    ## Turn a pandas DataFrame into GazeData.
    gd = saccades.GazeData(DF)

    ## Recenter.
    gd.center(origin=CENTER)

    ## Calculate velocity and acceleration.
    gd.get_accelerations()

    ## Display the data.
    print(gd)

    ## Save a plot.
    gd.plot(filename=IMAGE_PATH, reverse_y=True, show_raw=True)


#%% Script mode

if __name__ == '__main__':

    test_script()
    webbrowser.open(IMAGE_PATH)
