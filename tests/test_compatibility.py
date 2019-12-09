# -*- coding: utf-8 -*-

import os

import numpy
import plotnine

from . import constants


# Because subclassing the pandas DataFrame is complicated,
# we should make sure that its most useful functionality is preserved.
# So here we check that a few basic useful things
# that are possible with a pandas DataFrame
# are still possible with a GazeData instance.
# Most important are plotting and statistical summaries.


#%% pandas

def test_pandas_stats(gd_all):

    col_means = gd_all[['time', 'x', 'y']].mean()

    assert numpy.array_equal(col_means, constants.DF.mean())


# The dropna() method seems to be important for plotnine,
# so we should test that it works for GazeData too.
def test_pandas_dropna(gd_all):

    # Just check for exceptions.
    gd_all.dropna()


#%% plotnine

def test_plotnine_plot(gd):

    fig = (plotnine.ggplot(gd, plotnine.aes(x='x', y='y'))
           + plotnine.geom_point())  # noqa: W503

    fig.draw()

    filename = os.path.join(constants.IMAGES_PATH, 'test_compatibility.png')
    fig.save(filename, verbose=False)

    assert constants.image_file_ok(filename)
