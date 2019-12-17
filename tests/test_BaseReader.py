# -*- coding: utf-8 -*-

import pytest

from . import constants

from saccades.readers import BaseReader


# %% __init__()

def test_init(r_all):

    assert isinstance(r_all, BaseReader)


# %% row_pattern

@pytest.mark.parametrize('row', constants.VALID_ROWS)
def test_row_pattern_match(r, row):

    assert r.row_pattern.fullmatch(row) is not None


def test_row_pattern_groups(r):

    match = r.row_pattern.fullmatch('0 blah 1.0 2.0 blah')

    for num, col in enumerate(['time', 'x', 'y']):
        assert float(match.group(col)) == num


@pytest.mark.parametrize('row', constants.INVALID_ROWS)
def test_row_pattern_non_match(r, row):

    assert r.row_pattern.fullmatch(row) is None


# %% Context manager

def test_context_manager():

    with BaseReader(constants.DATA_FILES[0]['filepath']) as f:

        assert not f.file.closed

    assert f.file.closed
