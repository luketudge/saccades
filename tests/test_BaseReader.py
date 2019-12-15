# -*- coding: utf-8 -*-

import pytest

from . import constants

from saccades.readers import BaseReader


#%% __init__()

def test_init(r_all):

    assert isinstance(r_all, BaseReader)

    assert r_all.file.readable()
    assert not r_all.file.writable()


#%% Row regular expression

@pytest.mark.parametrize('row', constants.VALID_ROWS)
def test_row_pattern_match(r, row):

    assert r.row_pattern.fullmatch(row) is not None


@pytest.mark.parametrize('row', constants.INVALID_ROWS)
def test_row_pattern_non_match(r, row):

    assert r.row_pattern.fullmatch(row) is None
