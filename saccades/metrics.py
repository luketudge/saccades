# -*- coding: utf-8 -*-
"""Functions for calculating various parameters of gaze data.
"""

import numpy


SACCADE_METRICS = ['latency',
                   'duration',
                   'amplitude']


def latency(gd):
    """Latency of a saccade (a.k.a. saccadic reaction time).

    :param gd: Table of gaze data containing a saccade.
    :type gd: :class:`.gazedata.GazeData` \
    (or :class:`.gazedata.Saccade`)
    :return: Latency (in the units of the *time* column).
    :rtype: float
    """

    return gd['time'].iloc[0]


def duration(gd):
    """Duration of a saccade.

    :param gd: Table of gaze data containing a saccade.
    :type gd: :class:`.gazedata.GazeData` \
    (or :class:`.gazedata.Saccade`)
    :return: Duration (in the units of the *time* column).
    :rtype: float
    """

    return gd['time'].iloc[-1] - gd['time'].iloc[0]


def amplitude(gd):
    """Amplitude of a saccade.

    Result is converted to degrees of visual angle using \
    attributes `screen_res`, `screen_diag`, and `viewing_dist`, \
    unless the attribute `space_units` is `'dva'`, \
    in which case no conversion is performed.

    :param gd: Table of gaze data containing a saccade.
    :type gd: :class:`.gazedata.GazeData` \
    (or :class:`.gazedata.Saccade`)
    :return: Amplitude.
    :rtype: float
    """

    start_and_end = gd[['x', 'y']].iloc[[0, -1]]

    diffs = numpy.diff(start_and_end, axis=0)
    dist = numpy.linalg.norm(diffs)

    if gd.space_units != 'dva':
        dist = gd.px_to_dva(dist)

    return dist
