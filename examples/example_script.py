#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example script to test the current state of the saccades module.
"""

import os

import pandas
import plotnine

import saccades


base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_path = os.path.join(base_path, 'tests', 'data', 'example.csv')

df = pandas.read_csv(file_path, header=None)
gd = saccades.GazeData(df)

gd.get_accelerations()

print(gd)
