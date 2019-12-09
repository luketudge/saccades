# -*- coding: utf-8 -*-

import functools

import numpy
import pandas
import plotnine
import pytest

from . import constants

from saccades import gazedata


# GazeData methods that wrap functions from other modules
# are tested in the test files for those modules.
# Compatibility of GazeData with other data science packages
# is tested in test_compatibility.py.
# This test file tests the other features of the GazeData class.


#%% Setup

# Wrapped GazeData methods used in test_save_raw_coords_before_method_call().
methods = [functools.partial(gazedata.GazeData.center, origin=constants.ORIGIN),
           functools.partial(gazedata.GazeData.rotate, theta=constants.ANGLE)]


# An arbitrary function, used in test_detect_saccades().
def fun(x, val=True):

    return numpy.full(len(x), val)


#%% __init__()

def test_GazeData_init_types(gd_all):

    assert isinstance(gd_all, gazedata.GazeData)
    assert isinstance(gd_all, pandas.DataFrame)
    assert all((col in gd_all.columns) for col in ['time', 'x', 'y'])

    observed = gd_all[['time', 'x', 'y']]
    expected = constants.ARRAY[:, :3]

    assert numpy.array_equal(observed, expected)


@pytest.mark.parametrize('input_type', constants.INVALID_INIT_TYPES, ids=constants.INVALID_INIT_TYPE_NAMES)
def test_GazeData_invalid_init_types(input_type):

    with pytest.raises(ValueError):
        gazedata.GazeData(input_type)


def test_GazeData_empty_init():

    gd = gazedata.GazeData()

    assert isinstance(gd, gazedata.GazeData)
    assert isinstance(gd, pandas.DataFrame)
    assert list(gd.columns) == ['time', 'x', 'y']
    assert gd.empty


def test_GazeData_is_not_view():

    a = constants.ARRAY
    gd = gazedata.GazeData(a)
    gd['time'][0] = 9000.

    assert a[0, 0] != 9000.


#%% _save_raw_coords()

def test_save_raw_coords(gd):

    # Check first that the new columns aren't somehow already there.
    assert 'x_raw' not in gd
    assert 'y_raw' not in gd

    gd._save_raw_coords()

    assert numpy.array_equal(gd[['x_raw', 'y_raw']], gd[['x', 'y']])

    # Modify the coordinates and check that the raw ones are unharmed.
    gd['x'] = 0.
    assert not numpy.array_equal(gd['x_raw'], gd['x'])


# We would like this 'private' method to store the current coordinates
# but only if they have not already been stored.
# So here we test that there is no effect of a second call.

def test_save_raw_coords_with_existing_coords(gd):

    gd._save_raw_coords()
    gd['x'] = 0.
    gd._save_raw_coords()

    assert not numpy.array_equal(gd['x_raw'], gd['x'])


@pytest.mark.parametrize('method', methods)
def test_save_raw_coords_before_method_call(gd, method):

    method(gd)

    assert numpy.array_equal(gd[['x_raw', 'y_raw']], constants.ARRAY_XY)
    assert not numpy.array_equal(gd[['x_raw', 'y_raw']], gd[['x', 'y']])


#%% detect_saccades()

# Here we test just that detect_saccades() can take a function argument.
# Specific detection algorithms are tested in test_saccadedetection.py.

def test_detect_saccades(gd):

    assert 'saccade' not in gd

    gd.detect_saccades(fun)

    assert all(gd['saccade'])


def test_detect_saccades_with_keyword_arguments(gd):

    assert 'saccade' not in gd

    gd.detect_saccades(fun, val=False)

    assert not any(gd['saccade'])


#%% plot()

@pytest.mark.parametrize('kwargs', constants.PLOT_ARGS, ids=constants.PLOT_ARGS_NAMES)
def test_GazeData_plot(gd, kwargs):

    # Make a basic transform so as to distinguish data from raw data.
    gd.center(origin=constants.ORIGIN)

    fig = gd.plot(**kwargs)

    assert isinstance(fig, plotnine.ggplot)

    # Check inline rendering doesn't raise an exception.
    fig.draw()

    # Check image content is actually as expected.
    assert constants.image_file_ok(kwargs['filename'])


#%% Subsetting

# Subsetting instances of the GazeData class presents some challenges.
# We would like different subsetting operations to return different types.
# A subset of rows is still a valid table of gaze data.
# So this should return an instance of the GazeData class.
# A subset containing the 'time', 'x', and 'y' columns is also valid.
# So this column subset should also return an instance of the GazeData class.
# But a subset of other columns is an incomplete view of the data.
# So this should not return an instance of the GazeData class.

def test_subset_rows(gd_all):

    gd_subset = gd_all[:2]
    gd_subset = gd_subset[['time', 'x', 'y']]

    assert numpy.array_equal(gd_subset, constants.ARRAY[:2, :])
    assert isinstance(gd_subset, gazedata.GazeData)


def test_subset_rows_with_boolean(gd_all):

    gd_subset = gd_all[gd_all['time'] > gd_all['time'][0]]
    gd_subset = gd_subset[['time', 'x', 'y']]

    assert numpy.array_equal(gd_subset, constants.ARRAY[1:, :])
    assert isinstance(gd_subset, gazedata.GazeData)


def test_subset_complete_cols(gd_all):

    gd_subset = gd_all[['time', 'x', 'y']]

    assert numpy.array_equal(gd_subset, constants.ARRAY)
    assert isinstance(gd_subset, gazedata.GazeData)


def test_subset_rearranged_cols(gd_all):

    gd_subset = gd_all[['y', 'time', 'x']]
    gd_subset = gd_subset[['time', 'x', 'y']]

    assert numpy.array_equal(gd_subset, constants.ARRAY)
    assert isinstance(gd_subset, gazedata.GazeData)


def test_subset_extra_cols():

    gd = gazedata.GazeData(constants.DF_EXTRA_COLUMN)
    gd_subset = gd[['y', 'time', 'foo', 'x']]
    gd_subset = gd_subset[['time', 'x', 'y']]

    assert numpy.array_equal(gd_subset, constants.ARRAY)
    assert isinstance(gd_subset, gazedata.GazeData)


def test_subset_incomplete_cols(gd_all):

    gd_subset = gd_all[['x', 'y']]

    assert numpy.array_equal(gd_subset, constants.ARRAY_XY)
    assert not isinstance(gd_subset, gazedata.GazeData)
    assert isinstance(gd_subset, pandas.DataFrame)
