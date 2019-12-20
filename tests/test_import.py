# -*- coding: utf-8 -*-
"""Test that the contents of the modules are as expected.
"""


MAIN_CONTENTS = [
    'GazeData',
    'Saccade',
    'conversions',
    'geometry',
    'detection',
    'metrics',
    '__version__',
]

READERS_CONTENTS = [
    'Reader',
    'IViewReader',
]


def test_import():

    import saccades

    contents = dir(saccades)

    for name in MAIN_CONTENTS:
        assert name in contents


def test_import_readers():

    from saccades import readers

    contents = dir(readers)

    for name in READERS_CONTENTS:
        assert name in contents
