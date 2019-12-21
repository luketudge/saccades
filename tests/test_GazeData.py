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
import pytest

from saccades import GazeData


# %% Helper functions

def init_gazedata(data, **kwargs):
    """Initialize a GazeData table from a gaze data test case,
    with additional keyword arguments if necessary.
    """

    return GazeData(data['in']['data'], **kwargs)


# %% __init__()

def test_init(gaze_data):
    """Test initializing a GazeData table.

    It should be a subclass of pandas.DataFrame.
    The column names should be intact
    or replaced with time, x, and y if these are not supplied.
    """

    gd = init_gazedata(gaze_data)

    assert isinstance(gd, GazeData)
    assert isinstance(gd, pandas.DataFrame)
    assert set(gd.columns) == set(gaze_data['out']['columns'])
    assert numpy.array_equal(gd[['time', 'x', 'y']], gaze_data['out']['data'])


def test_invalid_init(invalid_gaze_data):
    """Check that invalid data raises the expected exception.
    """

    with pytest.raises(invalid_gaze_data['out']['exception']):
        init_gazedata(invalid_gaze_data)


def test_init_from_instance(gaze_data, attributes):
    """Test initializing a GazeData table from an existing instance.

    The attributes of the existing instance should be carried over.
    """

    gd = init_gazedata(gaze_data, **attributes['in']['attrs'])
    gd2 = GazeData(gd)

    for attr, val in attributes['out']['attrs'].items():
        assert getattr(gd2, attr) == val


def test_init_from_instance_new_attributes(gaze_data, attributes):
    """Test initializing a GazeData table from an existing instance,
    but setting new attributes at init.

    The attributes of the existing instance should be ignored.
    """

    new_value = 'bar'

    gd = init_gazedata(gaze_data, **attributes['in']['attrs'])
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


# %% Attributes

# Because pandas treats DataFrame attributes as columns by default,
# some wrangling is needed in order to store attributes in the normal way.
# So we should test that this works.

def test_has_attributes(gaze_data, attributes):
    """Check that a GazeData table has the attributes set at init.
    """

    gd = init_gazedata(gaze_data, **attributes['in']['attrs'])

    for attr, value in attributes['out']['attrs'].items():
        assert getattr(gd, attr) == value


def test_set_attributes(gaze_data, attributes):
    """Check that attributes can be set anew after init.
    """

    gd = init_gazedata(gaze_data)

    for attr, value in attributes['in']['attrs'].items():
        setattr(gd, attr, value)
        assert getattr(gd, attr) == attributes['out']['attrs'][attr]
