# -*- coding: utf-8 -*-
"""Test the Reader class.
"""

from saccades.readers import Reader


# %% __init__()

def test_init(file):

    r = file['in']['reader'](file['in']['filepath'], **file['in']['kwargs'])

    assert isinstance(r, Reader)


# %% header

def test_header(file):

    r = file['in']['reader'](file['in']['filepath'], **file['in']['kwargs'])

    assert r.header == file['out']['header']
