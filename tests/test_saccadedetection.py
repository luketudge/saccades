# -*- coding: utf-8 -*-

import pytest

from . import constants

from saccades import saccadedetection


@pytest.mark.parametrize('criteria', constants.CRITERIA)
def test_criterion(gd, criteria):

    # Pop out the 'exp' key.
    criteria = criteria.copy()
    expected = criteria.pop('exp')

    col = saccadedetection.criterion(gd, **criteria)

    assert all(col == expected)


def test_criterion_with_existing_column(gd):

    # Dummy velocity column filled with zeros.
    gd['velocity'] = 0.

    col = saccadedetection.criterion(gd, velocity=1.)

    assert not any(col)


def test_criterion_exceptions(gd):

    msg_pattern = 'Unrecognized metric'

    with pytest.raises(TypeError, match=msg_pattern):
        saccadedetection.criterion(gd, foo=9000.)

    with pytest.raises(TypeError, match=msg_pattern):
        saccadedetection.criterion(gd, velocity=22., foo=9000.)


@pytest.mark.parametrize('criteria', constants.CRITERIA)
def test_criterion_via_GazeData_method(gd, criteria):

    # Pop out the 'exp' key.
    criteria = criteria.copy()
    expected = criteria.pop('exp')

    gd.detect_saccades(saccadedetection.criterion, **criteria)

    assert all(gd['saccade'] == expected)
