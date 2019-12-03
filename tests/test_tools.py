# -*- coding: utf-8 -*-

import numpy
import pytest

from . import constants

from saccades import tools


#%% check_shape()

@pytest.mark.parametrize('input_type', constants.STANDARD_INIT_TYPES)
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
