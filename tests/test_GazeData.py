# -*- coding: utf-8 -*-

import functools

import numpy
import pandas
import plotnine
import pytest

from . import constants

from saccades import GazeData
from saccades import Saccade
from saccades import detection


# GazeData methods that wrap functions from other modules
# are tested in the test files for those modules.
# Compatibility of GazeData with other data science packages
# is tested in test_compatibility.py.
# This test file tests the other features of the GazeData class.


# %% Setup

# Wrapped GazeData methods used in test_save_raw_coords_before_method_call().
methods = [functools.partial(GazeData.center, origin=constants.ORIGIN),
           functools.partial(GazeData.rotate, theta=constants.ANGLE)]


# %% __init__()

def test_init_types(gd_all):

    assert isinstance(gd_all, GazeData)
    assert isinstance(gd_all, pandas.DataFrame)
    assert all((col in gd_all.columns) for col in ['time', 'x', 'y'])

    observed = gd_all[['time', 'x', 'y']]
    expected = constants.ARRAY[:, :3]

    assert numpy.array_equal(observed, expected)


@pytest.mark.parametrize('input_type', constants.INVALID_INIT_TYPES, ids=constants.INVALID_INIT_TYPE_NAMES)
def test_invalid_init_types(input_type):

    with pytest.raises(ValueError):
        GazeData(input_type)


def test_empty_init():

    gd = GazeData()

    assert isinstance(gd, GazeData)
    assert isinstance(gd, pandas.DataFrame)
    assert list(gd.columns) == ['time', 'x', 'y']
    assert gd.empty


def test_GazeData_is_not_view():

    a = constants.ARRAY
    gd = GazeData(a)
    gd['time'] = 9000.

    assert a[0, 0] != 9000.


# And I suppose we ought to be able to initialize from an existing instance.
# In this case, we want to keep its attributes.

def test_init_from_instance(gd_all):

    new_gd = GazeData(gd_all)

    for attr, val in constants.ATTRIBUTES.items():
        assert getattr(new_gd, attr) == val


# Unless the attributes are re-set explicitly in the __init__() call.

def test_init_from_instance_reset_attributes(gd_all):

    new_value = 'new_value'
    new_attributes = {attr: new_value for attr in constants.ATTRIBUTES}

    new_gd = GazeData(gd_all, **new_attributes)

    for attr in constants.ATTRIBUTES:
        assert getattr(new_gd, attr) == new_value


# %% _check_screen_info()

def test_check_screen_info(gd):

    gd._check_screen_info()


@pytest.mark.parametrize('attr', constants.SCREEN_ATTRIBUTES)
def test_check_screen_info_exceptions(gd, attr):

    setattr(gd, attr, None)

    with pytest.raises(AttributeError, match=attr):
        gd._check_screen_info()


# %% _save_raw_coords()

def test_save_raw_coords(gd):

    # Check first that the new columns aren't somehow already there.
    assert 'x_raw' not in gd
    assert 'y_raw' not in gd

    gd._save_raw_coords()

    assert numpy.array_equal(gd[['x_raw', 'y_raw']], gd[['x', 'y']])

    # Modify the coordinates and check that the raw ones are unharmed.
    gd['x'] = 0.
    assert not numpy.array_equal(gd['x_raw'], gd['x'])


# We would like this method to store the current coordinates
# only if they have not already been stored.
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


# %% viewing_parameters

def test_viewing_parameters(gd):

    params = gd.viewing_parameters

    assert params == constants.ATTRIBUTES


# %% reset_time()

def test_reset_time(gd_all):

    t_0 = constants.ARRAY[0, 0]
    t_end = constants.ARRAY[-1, 0]

    gd_all.reset_time()

    assert gd_all['time'].iloc[0] == 0.
    assert gd_all['time'].iloc[-1] == t_end - t_0


# %% detect_saccades()

# Here we test the general aspects of detect_saccades().
# Specific detection algorithms are tested in test_detection.py.

def test_detect_saccades(gd_all):

    gd_all['saccade'] = True

    result = gd_all.detect_saccades()

    assert len(result) == 1
    assert isinstance(result[0], GazeData)
    assert isinstance(result[0], Saccade)


@pytest.mark.parametrize('n', [0, 1, 2])
def test_detect_saccades_first_n(gd, n):

    # Add a dummy 'saccade' column with 2 saccades.
    sacc = numpy.full(len(gd), False)
    sacc[[0, -1]] = True
    gd['saccade'] = sacc

    result = gd.detect_saccades(n=n)

    assert len(result) == n


def test_detect_saccades_exception(gd):

    msg_pattern = 'Saccade detection function required but not supplied.'

    with pytest.raises(KeyError, match=msg_pattern):
        gd.detect_saccades()


def test_detect_saccades_with_function(gd):

    gd.detect_saccades(constants.fun)

    assert all(gd['saccade'])


def test_detect_saccades_with_keyword_argument(gd):

    result = gd.detect_saccades(constants.fun, val=False)

    assert result == []

    assert not any(gd['saccade'])


def test_detect_saccades_with_existing_saccade_column(gd):

    gd['saccade'] = False

    gd.detect_saccades(constants.fun)

    assert all(gd['saccade'])


# %% plot()

@pytest.mark.parametrize('kwargs', constants.PLOT_ARGS, ids=constants.PLOT_ARGS_NAMES)
def test_GazeData_plot(gd, kwargs):

    # Make a basic transform and add saccades,
    # so that all plot parameters have visible effects.
    gd.center(origin=constants.ORIGIN)
    gd.detect_saccades(detection.criterion,
                       velocity=constants.VELOCITY_LOW)

    fig = gd.plot(**kwargs)

    assert isinstance(fig, plotnine.ggplot)

    # Check inline rendering doesn't raise an exception.
    fig.draw()

    # Check image content is actually as expected.
    assert constants.image_file_ok(kwargs['filename'])


# %% Attributes

# Because pandas treats DataFrame attributes as columns by default,
# some wrangling is needed in order to store attributes in the normal way.
# So we should test that attributes can be set.

@pytest.mark.parametrize('attr, val', constants.ATTRIBUTES.items())
def test_has_attributes(gd_all, attr, val):

    assert getattr(gd_all, attr) == val


@pytest.mark.parametrize('attr, val', constants.ATTRIBUTES.items())
def test_set_attributes(gd_all, attr, val):

    new_value = 'new_value'
    setattr(gd_all, attr, new_value)

    assert getattr(gd_all, attr) == new_value


# %% Subsetting

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
    assert isinstance(gd_subset, GazeData)

    for attr, val in constants.ATTRIBUTES.items():
        assert getattr(gd_subset, attr) == val


def test_subset_rows_with_boolean(gd_all):

    gd_subset = gd_all[gd_all['time'] > gd_all['time'].iloc[0]]
    gd_subset = gd_subset[['time', 'x', 'y']]

    assert numpy.array_equal(gd_subset, constants.ARRAY[1:, :])
    assert isinstance(gd_subset, GazeData)

    for attr, val in constants.ATTRIBUTES.items():
        assert getattr(gd_subset, attr) == val


def test_subset_complete_cols(gd_all):

    gd_subset = gd_all[['time', 'x', 'y']]

    assert numpy.array_equal(gd_subset, constants.ARRAY)
    assert isinstance(gd_subset, GazeData)

    for attr, val in constants.ATTRIBUTES.items():
        assert getattr(gd_subset, attr) == val


def test_subset_rearranged_cols(gd_all):

    gd_subset = gd_all[['y', 'time', 'x']]
    gd_subset = gd_subset[['time', 'x', 'y']]

    assert numpy.array_equal(gd_subset, constants.ARRAY)
    assert isinstance(gd_subset, GazeData)

    for attr, val in constants.ATTRIBUTES.items():
        assert getattr(gd_subset, attr) == val


def test_subset_extra_cols():

    gd = GazeData(constants.DF_EXTRA_COLUMN, **constants.ATTRIBUTES)
    gd_subset = gd[['y', 'time', 'foo', 'x']]
    gd_subset = gd_subset[['time', 'x', 'y']]

    assert numpy.array_equal(gd_subset, constants.ARRAY)
    assert isinstance(gd_subset, GazeData)

    for attr, val in constants.ATTRIBUTES.items():
        assert getattr(gd_subset, attr) == val


def test_subset_incomplete_cols(gd_all):

    gd_subset = gd_all[['x', 'y']]

    assert numpy.array_equal(gd_subset, constants.ARRAY_XY)
    assert not isinstance(gd_subset, GazeData)
    assert isinstance(gd_subset, pandas.DataFrame)

    for attr in constants.ATTRIBUTES:
        assert not hasattr(gd_subset, attr)
