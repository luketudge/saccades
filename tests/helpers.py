# -*- coding: utf-8 -*-
"""Some helper functions used in more than one test module.
"""


def files_equal(file1, file2):
    """Determine whether two files have the same content.
    """

    bytes1 = open(file1, mode='rb').read()
    bytes2 = open(file2, mode='rb').read()

    return bytes1 == bytes2
