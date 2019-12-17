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


@pytest.mark.parametrize('row', constants.COLUMN_PATTERNS)
def test_row_pattern_groups(r, row):

    match = r.row_pattern.fullmatch(row)

    for num, col in enumerate(['time', 'x', 'y']):
        assert float(match.group(col)) == num


@pytest.mark.parametrize('row', constants.INVALID_ROWS)
def test_row_pattern_non_match(r, row):

    assert r.row_pattern.fullmatch(row) is None


# %% header

ids = [x['filename'] for x in constants.DATA_FILES]
@pytest.mark.parametrize('file', constants.DATA_FILES, ids=ids)
def test_header(file):

    kwargs = file.copy()
    header = kwargs.pop('header')

    for key in ['filename', 'data_start']:
        del kwargs[key]

    r = BaseReader(**kwargs)

    assert r.header == header
    assert r.file.closed


# %% Context manager

def test_context_manager():

    with BaseReader(constants.DATA_FILES[0]['file']) as r:
        assert not r.file.closed

    assert r.file.closed
