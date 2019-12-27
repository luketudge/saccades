# -*- coding: utf-8 -*-
"""Test the Saccade class.

Saccade attributes that call functions from the metrics module
are tested in the tests for that module.
"""

import numpy
import pandas
import pytest

from . import helpers

from saccades import GazeData
from saccades import Saccade


# %% __init__()

def test_init(gaze_data):
    """Test initializing a Saccade table.

    It should be an instance of the Saccade class,
    and a subclass of GazeData and pandas.DataFrame.
    """

    sacc = helpers.init_saccade(gaze_data)

    assert isinstance(sacc, Saccade)
    assert isinstance(sacc, GazeData)
    assert isinstance(sacc, pandas.DataFrame)


def test_init_from_GazeData(gaze_data):
    """Test initializing a Saccade table from an existing GazeData table.
    """

    gd = helpers.init_gazedata(gaze_data)
    sacc = Saccade(gd)

    assert isinstance(sacc, Saccade)
    assert isinstance(sacc, GazeData)
    assert isinstance(sacc, pandas.DataFrame)


# %% Indexing

# The Saccade class uses a different constructor,
# so we should test indexing just in case.

def test_indexing(gaze_data, index):
    """Test various kinds of indexing for getting subsets of data.
    """

    dummy_attr = 'foo'

    sacc = helpers.init_saccade(gaze_data, time_units=dummy_attr)
    subset = sacc.iloc[index['in']['rows']][index['in']['cols']]

    assert numpy.array_equal(subset, index['out']['data'])

    if index['out']['valid']:
        assert isinstance(subset, Saccade)
        assert subset.time_units == dummy_attr
    else:
        assert not isinstance(subset, Saccade)
        assert not isinstance(subset, GazeData)


# %% Attributes

def test_has_attributes(gaze_data, attributes):
    """Check that a Saccade table has the attributes set at init.
    """

    sacc = helpers.init_saccade(gaze_data, **attributes['in']['attrs'])

    for attr, value in attributes['out']['attrs'].items():
        assert getattr(sacc, attr) == value


def test_set_attributes(gaze_data, attributes):
    """Check that attributes can be set anew after init.
    """

    sacc = helpers.init_saccade(gaze_data)

    for attr, value in attributes['in']['attrs'].items():
        setattr(sacc, attr, value)
        assert getattr(sacc, attr) == attributes['out']['attrs'][attr]


def test_nonexistent_method(gaze_data_1):
    """Check that the automatic method searching
    does not find nonexistent methods.
    """

    sacc = helpers.init_saccade(gaze_data_1)

    with pytest.raises(AttributeError):
        sacc.nonexistent_method()
