# -*- coding: utf-8 -*-

from . import constants


def test_import():

    import saccades

    module_contents = dir(saccades)

    for name in constants.MODULE_CONTENTS:
        assert name in module_contents
