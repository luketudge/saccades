# -*- coding: utf-8 -*-
"""Algorithms for detecting saccades.
"""

import numpy


def criterion(gd, **criteria):
    """Extract saccades based on a simple cutoff.

    Keyword arguments take the form *metric=criterion*, \
    where *metric* is a column in `gd` \
    and *criterion* is a value for that column, \
    above which a sample is considered part of a saccade, \
    for example: *velocity=22, acceleration=8000*.

    Multiple metrics are combined with logical AND.

    Note that if no metrics are supplied, \
    by default all samples are marked as part of a saccade.

    Metrics that are not yet present in `gd` \
    but that are recognized as valid \
    are calculated automatically and added to `gd`.

    :param gd: A table of gaze data.
    :type gd: :class:`..GazeData`
    :return: Boolean column indicating whether each sample \
    is or is not part of a saccade.
    :rtype: numpy.ndarray
    :raises TypeError: If an unrecognized metric is requested.
    """

    # Start assuming all samples are saccades.
    result = numpy.full(len(gd), True)

    for metric, value in criteria.items():

        # Add recognized columns.
        if (metric == 'velocity') and ('velocity' not in gd):
            gd.get_velocities()
        elif (metric == 'acceleration') and ('acceleration' not in gd):
            gd.get_accelerations()

        elif metric not in gd:
            msg = 'Unrecognized metric {}.'
            raise(TypeError(msg.format(metric)))

        result[numpy.isnan(gd[metric])] = False
        result[gd[metric] <= value] = False

    return result
