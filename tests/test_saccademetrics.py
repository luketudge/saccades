# -*- coding: utf-8 -*-

from . import constants

from saccades import saccademetrics


# Just treat the whole GazeData test array as if it were a saccade.
# This means we can re-use a lot of the information in constants,
# rather than writing new values just for a saccade.


#%% latency()

def test_latency(gd):

    result = saccademetrics.latency(gd)

    assert result == constants.LATENCY
