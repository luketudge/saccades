# -*- coding: utf-8 -*-
"""Test that the contents of the modules are as expected.
"""


main_contents = [
    'GazeData',
    'Saccade',
    '__version__',
]

readers_contents = [
    'Reader',
]


def test_import():

    import saccades

    contents = dir(saccades)

    for name in main_contents:
        assert name in contents


def test_import_readers():

    from saccades import readers

    contents = dir(readers)

    for name in readers_contents:
        assert name in contents
