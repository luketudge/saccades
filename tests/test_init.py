# -*- coding: utf-8 -*-


def test_init():

    import saccades

    module_contents = dir(saccades)

    for name in ['GazeData', 'geometry', 'saccadedetection']:
        assert name in module_contents
