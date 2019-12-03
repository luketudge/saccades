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


#%% Setup

base_path = os.path.dirname(os.path.abspath(__file__))


#%% pandas

def test_pandas_plot(gd):

    # No assertion, just checking this at least doesn't error.
    gd.plot('x', 'y')
    gd.plot.line('x', 'y')


def test_pandas_stats(gd):

    col_means = gd[['time', 'x', 'y']].mean()

    assert numpy.array_equal(col_means, constants.DF.mean())


#%% plotnine

def test_plotnine_plot(gd_not_parametrized):

    fig = (plotnine.ggplot(gd_not_parametrized, plotnine.aes(x='x', y='y'))
           + plotnine.geom_point())  # noqa: W503

    fig.draw()

    fig.save(os.path.join(base_path, 'temp.png'), verbose=False)
