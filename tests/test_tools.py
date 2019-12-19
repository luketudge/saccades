# -*- coding: utf-8 -*-

import numpy
import pytest

from . import constants

from saccades import tools


# %% Setup

boolean_column = [False, True, True, True, False, False, True, False]
row_ids = list(range(len(boolean_column)))


# %% check_shape()

input_types = constants.STANDARD_INIT_TYPES.values()
ids = list(constants.STANDARD_INIT_TYPES.keys())
@pytest.mark.parametrize('input_type', input_types, ids=ids)
def test_check_shape(input_type):

    checked = tools.check_shape(input_type, constants.SHAPE)

    assert isinstance(checked, numpy.ndarray)
    assert numpy.array_equal(checked, constants.ARRAY)


@pytest.mark.parametrize('shape', constants.WILDCARD_SHAPES)
def test_check_shape_with_wildcard(shape):

    # No assertion, just checking we get no exceptions.
    tools.check_shape(constants.ARRAY, shape)


@pytest.mark.parametrize('shape', constants.WRONG_SHAPES)
def test_check_shape_exceptions(shape):

    with pytest.raises(ValueError):
        tools.check_shape(constants.ARRAY, shape)


# %% find_contiguous_subsets()

def test_find_contiguous_subsets():

    result = tools.find_contiguous_subsets(boolean_column)

    assert len(result) == 2
    assert row_ids[result[0]] == [1, 2, 3]
    assert row_ids[result[1]] == [6]


def test_find_contiguous_subsets_edge_cases():

    result = tools.find_contiguous_subsets([])
    assert len(result) == 0

    result = tools.find_contiguous_subsets([False])
    assert len(result) == 0

    result = tools.find_contiguous_subsets([False] * 9000)
    assert len(result) == 0
