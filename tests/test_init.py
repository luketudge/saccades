# -*- coding: utf-8 -*-


def test_init():

    import saccades

    for obj in ['GazeData', 'geometry']:
        assert obj in dir(saccades)
