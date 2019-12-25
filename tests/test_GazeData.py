# -*- coding: utf-8 -*-
"""Test the GazeData class.

GazeData methods that wrap functions from other modules
are tested in the test files for those modules.
Compatibility of GazeData objects with other data science packages
is tested in test_compatibility.py.
This test file tests the other features of the GazeData class.
"""

import numpy
import pandas
import plotnine
import pytest

from . import helpers

from saccades import GazeData
from saccades import Saccade


# %% __init__()

def test_init(gaze_data):
    """Test initializing a GazeData table.

    It should be a subclass of pandas.DataFrame.
    The column names should be intact
    or replaced with time, x, and y if these are not supplied.
    """

    gd = helpers.init_gazedata(gaze_data)

    assert isinstance(gd, GazeData)
    assert isinstance(gd, pandas.DataFrame)
    assert set(gd.columns) == set(gaze_data['out']['columns'])
    assert numpy.array_equal(gd[['time', 'x', 'y']], gaze_data['out']['data'])


def test_invalid_init(invalid_gaze_data):
    """Check that invalid data raises the expected exception.
    """

    with pytest.raises(invalid_gaze_data['out']['exception']):
        helpers.init_gazedata(invalid_gaze_data)


def test_init_from_instance(gaze_data, attributes):
    """Test initializing a GazeData table from an existing instance.

    The attributes of the existing instance should be carried over.
    """

    gd = helpers.init_gazedata(gaze_data, **attributes['in']['attrs'])
    gd2 = GazeData(gd)

    for attr, val in attributes['out']['attrs'].items():
        assert getattr(gd2, attr) == val


def test_init_from_instance_new_attributes(gaze_data, attributes):
    """Test initializing a GazeData table from an existing instance,
    but setting new attributes at init.

    The attributes of the existing instance should be ignored.
    """

    new_value = 'bar'

    gd = helpers.init_gazedata(gaze_data, **attributes['in']['attrs'])
    gd2 = GazeData(gd, **{attr: new_value for attr in attributes['in']['attrs']})

    for attr in attributes['out']['attrs']:
        assert getattr(gd2, attr) is new_value


def test_empty_init():
    """Test initializing a GazeData table without data.

    The columns time, x, and y should be initialized but empty.
    """

    gd = GazeData()

    assert set(gd.columns) == set(['time', 'x', 'y'])
    assert numpy.array_equal(gd, numpy.empty(shape=[0, 3]))


def test_GazeData_is_not_view():
    """Check that a GazeData table is not a view of the init data
    (i.e. that changes won't propagate back to the init data).
    """

    a = numpy.array([[0., 1., 2.],
                     [2., 3., 4.]])
    gd = GazeData(a)
    gd['time'] = 9000.

    assert a[0, 0] != 9000.


# %% Indexing

# Subsetting instances of the GazeData class presents some challenges.
# We would like different subsetting operations to return different types.
# A subset of rows is still a valid table of gaze data.
# So this should return an instance of the GazeData class.
# A subset containing the 'time', 'x', and 'y' columns is also valid.
# So this column subset should also return an instance of the GazeData class.
# But a subset of other columns is an incomplete view of the data.
# So this should not return an instance of the GazeData class.

def test_indexing(gaze_data, index):
    """Test various kinds of indexing for getting subsets of data.

    Subsets that get a complete gaze data table
    should return an instance of GazeDaza.
    Other subsets should revert to pandas DataFrame.

    GazeData subsets should preserve attributes.
    """

    dummy_attr = 'foo'

    gd = helpers.init_gazedata(gaze_data, time_units=dummy_attr)
    subset = gd.iloc[index['in']['rows']][index['in']['cols']]

    assert numpy.array_equal(subset, index['out']['data'])
    assert isinstance(subset, index['out']['type'])

    if index['out']['type'] == GazeData:
        assert gd.time_units == dummy_attr


# %% Attributes

# Because pandas treats DataFrame attributes as columns by default,
# some wrangling is needed in order to store attributes in the normal way.
# So we should test that this works.

def test_has_attributes(gaze_data, attributes):
    """Check that a GazeData table has the attributes set at init.
    """

    gd = helpers.init_gazedata(gaze_data, **attributes['in']['attrs'])

    for attr, value in attributes['out']['attrs'].items():
        assert getattr(gd, attr) == value


def test_set_attributes(gaze_data, attributes):
    """Check that attributes can be set anew after init.
    """

    gd = helpers.init_gazedata(gaze_data)

    for attr, value in attributes['in']['attrs'].items():
        setattr(gd, attr, value)
        assert getattr(gd, attr) == attributes['out']['attrs'][attr]


# %% _check_screen_info()

def test_check_screen_info(gaze_data_1, attributes):
    """Test checking the screen attributes.

    Incomplete groups of attributes should raise an exception,
    and the exception should mention which are missing.
    """

    gd = helpers.init_gazedata(gaze_data_1, **attributes['in']['attrs'])

    if attributes['out']['valid']:
        assert gd._check_screen_info() is None
    else:
        exception = attributes['out']['exception']
        error_msg = attributes['out']['error_msg']
        with pytest.raises(exception, match=error_msg):
            gd._check_screen_info()


# %% _save_raw_coords()

def test_save_raw_coords(gaze_data_1):
    """Test saving existing coordinates into new columns.

    The new columns should have the same values,
    and they should not be views of the existing columns.
    A second call should have no effect,
    since the original values have already been saved.
    """

    gd = helpers.init_gazedata(gaze_data_1)
    gd._save_raw_coords()

    assert numpy.array_equal(gd[['x_raw', 'y_raw']], gd[['x', 'y']])

    gd['x'] = 9000.
    assert not numpy.array_equal(gd['x_raw'], gd['x'])

    gd._save_raw_coords()
    assert not numpy.array_equal(gd['x_raw'], gd['x'])


def test_save_raw_coords_before_method_call(gaze_data_1, method):
    """Test saving existing coordinates into new columns
    automatically before some method calls.

    The new columns should have the old values of the original columns,
    and the original columns should now have different values.
    """

    gd = helpers.init_gazedata(gaze_data_1)
    method['in']['method'](gd)

    if method['out']['saves_coords']:
        saved_coords = gd[['time', 'x_raw', 'y_raw']]
        new_coords = gd[['time', 'x', 'y']]
        assert numpy.array_equal(saved_coords, gaze_data_1['out']['data'])
        assert not numpy.array_equal(saved_coords, new_coords)
    else:
        for col in ['x_raw', 'y_raw']:
            assert col not in gd


# %% viewing_parameters

def test_viewing_parameters(gaze_data_1, attributes):
    """Test getting the dictionary of viewing parameters.
    """

    gd = helpers.init_gazedata(gaze_data_1, **attributes['in']['attrs'])
    params = gd.viewing_parameters

    assert params == attributes['out']['attrs']


# %% reset_time()

def test_reset_time(gaze_data):
    """Test resetting the time column to start at 0.
    """

    t_0 = gaze_data['out']['data'][0, 0]
    t_end = gaze_data['out']['data'][-1, 0]

    gd = helpers.init_gazedata(gaze_data)
    gd.reset_time()

    assert gd['time'].iloc[0] == 0.
    assert gd['time'].iloc[-1] == t_end - t_0


# %% detect_saccades()

def test_detect_saccades(gaze_data_1, detection):
    """Test detecting saccades.

    The saccade column should reflect the output of the supplied function.
    The return value should have length equal to the number of saccades.
    Each item should be an instance of the Saccade class.
    The saccades should preserve the attributes of the GazeData table.
    """

    dummy_attr = 'foo'

    gd = helpers.init_gazedata(gaze_data_1, time_units=dummy_attr)
    result = gd.detect_saccades(detection['in']['func'],
                                detection['in']['n'],
                                **detection['in']['kwargs'])

    assert all(gd['saccade'] == detection['out']['column'])
    assert len(result) == detection['out']['n']

    for item in result:
        assert isinstance(item, Saccade)
        assert item.time_units == dummy_attr


def test_detect_saccades_without_function(gaze_data_1):
    """Test detecting saccades when no detection function is supplied.

    If the saccade column exists, it should be used instead.
    If the saccade column does not exist, an exception should be raised.
    """

    gd = helpers.init_gazedata(gaze_data_1)

    with pytest.raises(KeyError, match='function required'):
        gd.detect_saccades()
    assert 'saccade' not in gd

    gd['saccade'] = True
    result = gd.detect_saccades()
    assert len(result) == 1


# %% plot()

@pytest.mark.slow
def test_plot(plot):
    """Test plotting by comparing to reference plot images.
    """

    gd = helpers.init_gazedata(plot)

    for func in plot['in']['transform']:
        func(gd)

    fig = gd.plot(filename=plot['in']['filepath'],
                  **plot['in']['kwargs'])

    assert isinstance(fig, plotnine.ggplot)

    fig.draw()

    assert helpers.files_equal(plot['in']['filepath'], plot['out']['filepath'])
