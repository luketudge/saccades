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

from saccades import GazeData
from saccades.saccadedetection import criterion


#%% Setup

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

DATA_FILENAME = 'example.csv'
DATA_PATH = os.path.join(BASE_PATH, 'data', DATA_FILENAME)

OUTPUT_FILENAME = 'example_saccade.csv'
OUTPUT_PATH = os.path.join(BASE_PATH, OUTPUT_FILENAME)

DF = pandas.read_csv(DATA_PATH, header=None)

CENTER = (320., 240.)
SCREEN_RES = (640., 480.)
SCREEN_DIAG = 42.
VIEWING_DIST = 100.

VELOCITY_CRITERION = 0.022

IMAGE_FILENAME = 'example_saccade_plot.png'
IMAGE_PATH = os.path.join(BASE_PATH, IMAGE_FILENAME)


#%% Test function

def test_script():

    ## Turn a pandas DataFrame into GazeData.
    gd = GazeData(DF, time_units='ms', space_units='px',
                  screen_res=SCREEN_RES,
                  screen_diag=SCREEN_DIAG,
                  viewing_dist=VIEWING_DIST)

    ## Reset time index.
    gd.reset_time()

    ## Recenter.
    gd.center(origin=CENTER)

    ## Calculate velocity and acceleration.
    gd.get_accelerations()

    ## Display the data.
    print(gd)

    ## Get first saccade.
    first_saccade = gd.detect_saccades(criterion,
                                       n=1,
                                       velocity=VELOCITY_CRITERION)[0]
    print(first_saccade)

    ## Save first saccade to csv.
    first_saccade.to_csv(OUTPUT_PATH, index=False)

    ## Save a plot.
    gd.plot(filename=IMAGE_PATH,
            reverse_y=True,
            show_raw=True,
            saccades=True)


#%% Script mode

if __name__ == '__main__':

    test_script()
    webbrowser.open(IMAGE_PATH)
