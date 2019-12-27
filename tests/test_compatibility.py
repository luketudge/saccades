# -*- coding: utf-8 -*-
"""Test that the GazeData class preserves features of pandas DataFrames.
"""

import numpy
import plotnine
import pytest

from . import helpers


# %% dropna()

def test_pandas_dropna(nans):
    """Check that the pandas DataFrame method dropna()
    also works for GazeData tables.

    Dropping NA values for a column with no NA values
    should leave the data intact.
    Otherwise, rows with any NA values should be removed.
    """

    gd = helpers.init_gazedata(nans)
    subset = gd.dropna(subset=nans['in']['subset'])

    assert numpy.allclose(subset, nans['out']['data'], equal_nan=True)


# %% Statistical summaries

def test_pandas_stats(gaze_data):
    """Check that pandas statistical summaries
    also work for GazeData tables.
    """

    gd = helpers.init_gazedata(gaze_data)
    colmeans = gd[['time', 'x', 'y']].mean()

    assert numpy.array_equal(colmeans, gaze_data['out']['colmeans'])


# %% ggplot

@pytest.mark.slow
def test_plotnine_plot(gaze_data):
    """Check that GazeData tables can be used in ggplots
    with plotnine.

    The plot should be rendered without raising an exception.
    """

    gd = helpers.init_gazedata(gaze_data)

    fig = (plotnine.ggplot(gd, plotnine.aes(x='x', y='y'))
           + plotnine.geom_point())  # noqa: W503
    fig.draw()
