# -*- coding: utf-8 -*-

from . import constants

from saccades import metrics


# %% latency()

def test_latency(sacc):

    result = metrics.latency(sacc)

    assert result == constants.LATENCY


def test_latency_as_Saccade_method(sacc):

    result = sacc.latency()

    assert result == constants.LATENCY


# %% duration()

def test_duration(sacc):

    result = metrics.duration(sacc)

    assert result == constants.DURATION


def test_duration_as_Saccade_method(sacc):

    result = sacc.duration()

    assert result == constants.DURATION


# %% amplitude()

def test_amplitude(sacc):

    result = metrics.amplitude(sacc)

    assert result == constants.AMPLITUDE_DVA


def test_amplitude_with_dva_units(sacc):

    sacc.space_units = 'dva'

    result = metrics.amplitude(sacc)

    assert result == constants.AMPLITUDE


def test_amplitude_as_Saccade_method(sacc):

    result = sacc.amplitude()

    assert result == constants.AMPLITUDE_DVA
