# -*- coding: utf-8 -*-

from saccades.readers import BaseReader


#%% __init__()

def test_init(r):

    assert isinstance(r, BaseReader)
