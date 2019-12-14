# -*- coding: utf-8 -*-

from saccades.readers import BaseReader


#%% __init__()

def test_init(r_all):

    assert isinstance(r_all, BaseReader)

    assert r_all.file.readable()
    assert not r_all.file.writable()
