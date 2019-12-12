# -*- coding: utf-8 -*-

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


#%% Subsetting

# Subsetting a saccade doesn't really make sense,
# so subsets should just revert to being normal GazeData.

def test_subset_rows(sacc):

    sacc_subset = sacc[:2]

    assert not isinstance(sacc_subset, Saccade)
    assert isinstance(sacc_subset, GazeData)
