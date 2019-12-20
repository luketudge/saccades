# -*- coding: utf-8 -*-
"""Test the Reader class.
"""

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

def test_init(file):

    r = init_reader(file)

    assert isinstance(r, Reader)


# %% header

def test_header(file):

    r = init_reader(file)

    assert r.header == file['out']['header']
