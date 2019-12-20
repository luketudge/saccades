# -*- coding: utf-8 -*-
"""Test the Reader class.
"""

import types

import numpy
import pytest
import regex

from saccades import GazeData
from saccades.readers import Reader


# %% Helper functions

def init_reader(file, **kwargs):
    """Initialize a Reader from a data file test case,
    with additional keyword arguments if necessary.
    """

    reader = file['in']['reader']
    filepath = file['in']['filepath']

    return reader(filepath, **file['in']['kwargs'], **kwargs)


# %% __init__()

def test_init(data_file):

    r = init_reader(data_file)

    assert isinstance(r, Reader)


# %% row_pattern

def test_row_pattern(data_file, row_format):

    r = init_reader(data_file)
    row = row_format['in']['row']

    if 'sep' in data_file['in']:
        row = regex.sub(r'\s', data_file['in']['sep'], row)

    match = r.row_pattern.fullmatch(row)

    if row_format['out']['valid']:
        values = [abs(float(match.group(col))) for col in ['time', 'x', 'y']]
        assert values == row_format['out']['values']
    else:
        assert match is None


# %% header

def test_header(data_file):

    r = init_reader(data_file)

    assert r.header == data_file['out']['header']


# %% process_messages()

def test_process_messages(data_file):

    r = init_reader(data_file)
    messages = 'foo'

    assert r.process_messages(messages) == messages


# %% process_data()

def test_process_data(data_file, data_block):

    kwargs = {}

    if 'na_values' in data_block['in']:
        kwargs['na_values'] = data_block['in']['na_values']

    r = init_reader(data_file, **kwargs)
    messages = 'foo'
    gd = r.process_data(data_block['in']['data'], messages)

    assert isinstance(gd, GazeData)
    assert gd.messages == messages

    # We have to use allclose() here,
    # as array_equal() returns False if any values are NaN.
    assert numpy.allclose(gd, data_block['out']['data'], equal_nan=True)


# %% get_blocks()

@pytest.mark.slow
def test_get_blocks(data_file):

    r = init_reader(data_file)
    blocks = r.get_blocks()

    assert isinstance(blocks, types.GeneratorType)

    block_count = 0

    for b in blocks:
        block_count = block_count + 1
        assert isinstance(b, GazeData)

    if 'n_blocks' in data_file['out']:
        assert block_count == data_file['out']['n_blocks']

    assert r.file.closed


# %% Context manager

def test_context_manager(data_file):

    with init_reader(data_file) as r:
        assert not r.file.closed

    assert r.file.closed
