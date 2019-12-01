# -*- coding: utf-8 -*-

import numpy
import pytest

from . import constants

from saccades import tools


#%% Anything

def test_Anything():

    for val in [True, False, None, 0, 1, '', 'foo', numpy.nan]:
        assert tools.Anything() == val
        assert not (tools.Anything() != val)


#%% check_shape()

def test_check_shape_correct_shape():

    checked = tools.check_shape(constants.ARRAY, constants.SHAPE)
    assert numpy.array_equal(checked, constants.ARRAY)


def test_check_shape_with_None():

    # No assertion, just checking we get no exceptions.
    for shape in [(None, constants.SHAPE[1]), (constants.SHAPE[0], None), (None, None)]:
        tools.check_shape(constants.ARRAY, shape)


def test_check_shape_exceptions_ndim():

    # Too many dimensions.
    for shape in [(constants.SHAPE[0],), (None,)]:
        with pytest.raises(ValueError):
            tools.check_shape(constants.ARRAY, shape)

    # Too few dimensions.
    for extra_dim in [2, None]:
        with pytest.raises(ValueError):
            tools.check_shape(constants.ARRAY, constants.SHAPE + (extra_dim,))


def test_check_shape_exceptions_size():

    wrong_shape = tuple(x + 1 for x in constants.SHAPE)

    for shape in [wrong_shape, (wrong_shape[0], None), (None, wrong_shape[1])]:
        with pytest.raises(ValueError):
            tools.check_shape(constants.ARRAY, shape)


def test_check_shape_return_type():

    for input_type in [constants.SEQUENCE, constants.ARRAY]:
        checked = tools.check_shape(input_type, constants.SHAPE)
        assert isinstance(checked, numpy.ndarray)
