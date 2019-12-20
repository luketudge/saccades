# -*- coding: utf-8 -*-

import os

import numpy
import pytest
import regex

from . import constants

from saccades.readers import BaseReader
from saccades.readers.regexes import FILLER
from saccades.readers.regexes import FLOAT
from saccades.readers.regexes import NUMBER
from saccades.readers.regexes import POS_INTEGER


# %% Setup subclass



@pytest.fixture
def new_r():

    filepath = os.path.join(constants.DATA_PATH, constants.DATA_FILE_SUBCLASS)

    return NewReader(filepath)


# %% Test functions

def test_init(new_r):

    assert isinstance(new_r, BaseReader)
    assert isinstance(new_r, NewReader)


# The innovation in the subclass is to allow integer x and y values.
# So test for this.

def test_row_pattern(new_r):

    assert new_r.row_pattern.fullmatch('1 2.0 3.0') is not None
    assert new_r.row_pattern.fullmatch('1 2 3') is not None
    assert new_r.row_pattern.fullmatch('1.0 2 3') is None


def test_process_header(new_r):

    assert new_r.header == constants.HEADER_SUBCLASS


def test_process_data(new_r):

    data = {'time': ['0'], 'x': ['1'], 'y': ['2']}
    messages = 'foo'

    gd = new_r.process_data(data, messages)

    assert gd.messages == messages
    assert gd.screen_res == constants.HEADER_SUBCLASS['screen_res']
    assert gd.screen_diag == constants.HEADER_SUBCLASS['screen_diag']
    assert gd.viewing_dist == constants.HEADER_SUBCLASS['viewing_dist']


def test_get_blocks(new_r):

    blocks = list(new_r.get_blocks())

    assert len(blocks) == 1

    assert blocks[0].screen_res == constants.HEADER_SUBCLASS['screen_res']
    assert blocks[0].screen_diag == constants.HEADER_SUBCLASS['screen_diag']
    assert blocks[0].viewing_dist == constants.HEADER_SUBCLASS['viewing_dist']
