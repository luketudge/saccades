#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example script to test the current state of the saccades module.
"""

import os

import pandas
import plotnine

import saccades


filepath = os.path.join('data', 'example.csv')
df = pandas.read_csv(filepath, header=None)
gd = saccades.GazeData(df)

print(gd)
