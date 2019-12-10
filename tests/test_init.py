# -*- coding: utf-8 -*-

from . import constants


def test_init():

    import saccades

    module_contents = dir(saccades)

    for name in constants.MODULE_CONTENTS:
        assert name in module_contents
