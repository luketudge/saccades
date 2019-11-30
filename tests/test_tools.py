# -*- coding: utf-8 -*-

import numpy
import pytest

from saccades import tools


#%% Setup

ARRAY = [[0, 1],
         [2, 3],
         [4, 5]]

SHAPE = (3, 2)


#%% Anything

def test_Anything():

    for val in [True, False, None, 0, 1, '', 'foo', numpy.nan]:
        assert tools.Anything() == val
        assert not (tools.Anything() != val)


#%% check_shape

def test_check_shape():

    # Should produce no exeption.
    checked_array = tools.check_shape(ARRAY, SHAPE)

    # And check that the array is unharmed.
    assert numpy.array_equal(checked_array, ARRAY)


def test_check_shape_return_type():

    # Sequence in, numpy array out.
    checked_array = tools.check_shape(ARRAY, SHAPE)
    assert isinstance(checked_array, numpy.ndarray)

    # numpy array in, numpy array out.
    checked_array = tools.check_shape(numpy.array(ARRAY), SHAPE)
    assert isinstance(checked_array, numpy.ndarray)


def test_check_shape_with_None():

    # No assertion, just checking we get no exceptions.
    for shape in [(None, SHAPE[1]), (SHAPE[0], None), (None, None)]:
        tools.check_shape(ARRAY, shape)


def test_check_shape_exceptions_ndim():

    # Too many dimensions.
    for shape in [(SHAPE[0],), (None,)]:
        with pytest.raises(ValueError):
            tools.check_shape(ARRAY, shape)

    # Too few dimensions.
    for extra_dim in [2, None]:
        with pytest.raises(ValueError):
            tools.check_shape(ARRAY, SHAPE + (extra_dim,))


def test_check_shape_exceptions_size():

    wrong_shape = tuple(x + 1 for x in SHAPE)

    for shape in [wrong_shape, (wrong_shape[0], None), (None, wrong_shape[1])]:
        with pytest.raises(ValueError):
            tools.check_shape(ARRAY, shape)
