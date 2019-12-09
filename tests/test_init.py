# -*- coding: utf-8 -*-


def test_init():

    import saccades

    module_contents = dir(saccades)

    for name in ['GazeData', 'algorithms']:
        assert name in module_contents


def test_import_submodules():

    from saccades import algorithms  # noqa: F401
    from saccades.algorithms import saccadedetection  # noqa: F401
