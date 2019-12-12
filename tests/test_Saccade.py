# -*- coding: utf-8 -*-

import numpy
import pandas
import pytest

from . import constants

from saccades import GazeData
from saccades import Saccade


#%% __init__()

def test_init_from_GazeData(gd_all):

    sacc = Saccade(gd_all)

    assert isinstance(sacc, Saccade)
    assert isinstance(sacc, GazeData)
    assert isinstance(sacc, pandas.DataFrame)


#%% Attributes

@pytest.mark.parametrize('attr, val', constants.ATTRIBUTES.items())
def test_has_attributes(sacc, attr, val):

    assert getattr(sacc, attr) == val


@pytest.mark.parametrize('attr, val', constants.ATTRIBUTES.items())
def test_set_attributes(sacc, attr, val):

    new_value = 'new_value'
    setattr(sacc, attr, new_value)

    assert getattr(sacc, attr) == new_value


@pytest.mark.parametrize('attr, val', constants.ATTRIBUTES.items())
def test_preserve_parent_attributes(gd, attr, val):

    # Add a dummy 'saccade' column with 2 saccades.
    saccade = numpy.full(len(gd), False)
    saccade[[0, -1]] = True
    gd['saccade'] = saccade

    all_saccades = gd.detect_saccades()

    for sacc in all_saccades:
        assert getattr(sacc, attr) == val


# And just in case, check that the auto-method wrangling
# still correctly reports non-existent methods as missing.
def test_nonexistent_method(sacc):

    with pytest.raises(AttributeError):
        sacc.nonexistent_method()


#%% Subsetting

def test_subset_rows(sacc):

    sacc_subset = sacc[:2]

    assert isinstance(sacc_subset, Saccade)


def test_subset_complete_cols(sacc):

    sacc_subset = sacc[['time', 'x', 'y']]

    assert isinstance(sacc_subset, Saccade)


def test_subset_incomplete_cols(sacc):

    sacc_subset = sacc[['x', 'y']]

    assert not isinstance(sacc_subset, Saccade)
    assert not isinstance(sacc_subset, GazeData)
    assert isinstance(sacc_subset, pandas.DataFrame)
