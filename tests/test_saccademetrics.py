# -*- coding: utf-8 -*-

from . import constants

from saccades import saccademetrics


#%% latency()

def test_latency(sacc):

    result = saccademetrics.latency(sacc)

    assert result == constants.LATENCY


def test_latency_as_Saccade_method(sacc):

    result = sacc.latency()

    assert result == constants.LATENCY
