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

class NewReader(BaseReader):

    # The data row pattern for this file is:
    # POS_INTEGER NUMBER NUMBER FILLER
    # So we override the corresponding method.
    def build_row_pattern(self):

        row_groups = ['(?P<time>{})', '(?P<x>{})', '(?P<y>{})']
        row_groups = self.sep.join(row_groups)

        return row_groups.format(POS_INTEGER, NUMBER, NUMBER) + FILLER

    # The final line of the header gives information
    # about the viewing distance and screen dimensions.
    # So we override the appropriate method for this too.
    def process_header(self, header):

        final_row = header.splitlines()[-1]

        info = {}

        for item in ['distance', 'width', 'height']:
            pattern = '{} ({})'.format(item, FLOAT)
            match = regex.search(pattern, final_row)
            info[item] = float(match.group(1))

        screen_diag = numpy.linalg.norm([info['width'], info['height']])

        return {'viewing_dist': info['distance'], 'screen_diag': screen_diag}

    # And we would like to put the header information into each block.
    # So finally we override the method for this.
    def process_data(self, data, messages):

        gd = super().process_data(data, messages)

        gd.screen_diag = self.header['screen_diag']
        gd.viewing_dist = self.header['viewing_dist']

        return gd


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
    assert gd.screen_diag == constants.HEADER_SUBCLASS['screen_diag']
    assert gd.viewing_dist == constants.HEADER_SUBCLASS['viewing_dist']


def test_get_blocks(new_r):

    blocks = list(new_r.get_blocks())

    assert len(blocks) == 1
    assert blocks[0].screen_diag == constants.HEADER_SUBCLASS['screen_diag']
