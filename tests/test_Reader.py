# -*- coding: utf-8 -*-
"""Test the Reader class.
"""

import regex

from saccades.readers import Reader


# %% Helper functions

def init_reader(data_file, **kwargs):
    """Initialize a Reader from a data file test case,
    with additional keyword arguments if necessary.
    """

    reader = data_file['in']['reader']
    filepath = data_file['in']['filepath']

    return reader(filepath, **data_file['in']['kwargs'], **kwargs)


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
        assert match is not None
    else:
        assert match is None


# %% header

def test_header(data_file):

    r = init_reader(data_file)

    assert r.header == data_file['out']['header']
