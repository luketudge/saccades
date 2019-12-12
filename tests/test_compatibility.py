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


#%% pandas.DataFrame.dropna()

# Check for exceptions with the default arguments.
def test_pandas_dropna(gd_all):

    gd_all.dropna()


# Check that dropna() also actually works.
# The first row should have NaN for velocity after get_accelerations(),
# so dropna should remove this row.
def test_pandas_dropna_subset(gd_all):

    gd_all.get_accelerations()
    gd_subset = gd_all.dropna(subset=['velocity'])

    assert len(gd_all) - len(gd_subset) == 1


#%% pandas.DataFrame.mean()

def test_pandas_stats(gd_all):

    col_means = gd_all[['time', 'x', 'y']].mean()

    assert numpy.array_equal(col_means, constants.DF.mean())


#%% plotnine.ggplot()

def test_plotnine_plot(gd):

    fig = (plotnine.ggplot(gd, plotnine.aes(x='x', y='y'))
           + plotnine.geom_point())  # noqa: W503

    fig.draw()

    filename = 'test_plotnine_compatibility.png'
    filepath = os.path.join(constants.IMAGES_PATH, filename)
    fig.save(filepath, verbose=False)

    assert constants.image_file_ok(filepath)
