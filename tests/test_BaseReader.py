# -*- coding: utf-8 -*-

import types

import numpy
import pytest

from . import constants

from saccades import GazeData
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

@pytest.mark.parametrize('file', constants.DATA_FILES, ids=constants.DATA_FILE_IDS)
def test_header(file):

    kwargs = constants.get_basereader_args(file)
    r = BaseReader(**kwargs)

    assert r.header == file['header']
    assert r.file.closed


# %% 'Dummy' methods.

def test_process_header(r):

    header = 'foo'

    assert r.process_header(header) == header


def test_process_messages(r):

    messages = 'foo'

    assert r.process_messages(messages) == messages


@pytest.mark.parametrize('df', [constants.DF, constants.DF_STRINGS], ids=['float', 'str'])
def test_process_data(r, df):

    messages = 'foo'

    gd = r.process_data(df, messages)

    assert isinstance(gd, GazeData)
    assert numpy.array_equal(gd, constants.ARRAY)
    assert gd.messages == messages


# %% get_blocks()

@pytest.mark.parametrize('file', constants.DATA_FILES, ids=constants.DATA_FILE_IDS)
def test_get_blocks(file):

    kwargs = constants.get_basereader_args(file)
    r = BaseReader(**kwargs)

    blocks = r.get_blocks()

    assert isinstance(blocks, types.GeneratorType)

    block_count = 0

    for b in blocks:

        assert isinstance(b, GazeData)

        if block_count == 0:
            assert b.messages == file['header']

        block_count = block_count + 1

    if 'n_blocks' in file:
        assert block_count == file['n_blocks']

    assert r.file.closed


# %% Context manager

def test_context_manager():

    with BaseReader(constants.DATA_FILES[0]['file']) as r:
        assert not r.file.closed

    assert r.file.closed
