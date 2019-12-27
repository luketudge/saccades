# -*- coding: utf-8 -*-
"""Test cases for conversions.
"""


# %% _viewing_dist_to_px()

VD2PX = {
    '0': {
        'in': {'dist': 4., 'res': [4., 3.], 'diag': 2.},
        'out': {'px': 10.}
    },
}


# %% px_to_dva()

PX2DVA = {
    '0': {
        'in': {'res': [4., 3.], 'diag': 2., 'dist': 4.,
               'px': [0., 10.], 'dva': [0., 45.]},
        'out': {'px': [0., 10.], 'dva': [0., 45.]}
    },
}
