# -*- coding: utf-8 -*-

import pytest

from . import constants

from saccades.readers import BaseReader


#%% __init__()

def test_init(r_all):

    assert isinstance(r_all, BaseReader)

    assert r_all.file.readable()
    assert not r_all.file.writable()


#%% row_pattern

@pytest.mark.parametrize('row', constants.VALID_ROWS)
def test_row_pattern_match(r, row):

    assert r.row_pattern.fullmatch(row) is not None


def test_row_pattern_groups(r):

    match = r.row_pattern.fullmatch('0 1.0 2.0')

    for num, col in enumerate(['time', 'x', 'y']):
        assert float(match.group(col)) == num


@pytest.mark.parametrize('row', constants.INVALID_ROWS)
def test_row_pattern_non_match(r, row):

    assert r.row_pattern.fullmatch(row) is None
