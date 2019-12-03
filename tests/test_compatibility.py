# -*- coding: utf-8 -*-

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

def test_pandas_plot(gd):

    # No assertion, just checking this at least doesn't error.
    gd.plot('x', 'y')
    gd.plot.line('x', 'y')


def test_pandas_stats(gd):

    assert numpy.array_equal(gd.mean(), constants.DATAFRAME.mean())
    assert numpy.array_equal(gd.median(), constants.DATAFRAME.median())


#%% plotnine

def test_plotnine_plot(gd):

    fig = plotnine.ggplot(gd, plotnine.aes(x='x', y='y'))
    fig.draw()
    fig.save('temp.png')
