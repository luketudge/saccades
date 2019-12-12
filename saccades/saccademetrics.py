# -*- coding: utf-8 -*-
"""Functions for calculating various parameters of a saccade.
"""


def latency(gd):
    """Latency of a saccade (a.k.a. saccadic reaction time).

    :param gd: Table of gaze data containing a saccade.
    :type gd: :class:`.gazedata.GazeData`
    :return: Latency.
    :rtype: float
    """

    return gd['time'].iloc[0]
