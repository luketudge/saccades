# -*- coding: utf-8 -*-

from . import constants

from saccades import saccademetrics


#%% latency()

def test_latency(sacc):

    result = saccademetrics.latency(sacc)

    assert result == constants.LATENCY
