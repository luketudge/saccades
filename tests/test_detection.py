# -*- coding: utf-8 -*-

import pytest

from . import constants

from saccades import detection


@pytest.mark.parametrize('criteria', constants.CRITERIA)
def test_criterion(gd, criteria):

    # Pop out the 'exp' key.
    criteria = criteria.copy()
    expected = criteria.pop('exp')

    col = detection.criterion(gd, **criteria)

    assert all(col == expected)


def test_criterion_with_existing_column(gd):

    # Dummy velocity column filled with zeros.
    gd['velocity'] = 0.

    col = detection.criterion(gd, velocity=1.)

    assert not any(col)


def test_criterion_exceptions(gd):

    msg_pattern = 'Unrecognized metric'

    with pytest.raises(TypeError, match=msg_pattern):
        detection.criterion(gd, foo=9000.)

    with pytest.raises(TypeError, match=msg_pattern):
        detection.criterion(gd, velocity=22., foo=9000.)


@pytest.mark.parametrize('criteria', constants.CRITERIA)
def test_criterion_as_GazeData_method(gd, criteria):

    # Pop out the 'exp' key.
    criteria = criteria.copy()
    expected = criteria.pop('exp')

    gd.detect_saccades(detection.criterion, **criteria)

    assert all(gd['saccade'] == expected)
