# -*- coding: utf-8 -*-

from . import constants


def test_import():

    import saccades

    module_contents = dir(saccades)

    for name in constants.MODULE_CONTENTS:
        assert name in module_contents


def test_import_submodule():

    from saccades import readers

    module_contents = dir(readers)

    for name in constants.READERS_CONTENTS:
        assert name in module_contents
