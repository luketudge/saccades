# -*- coding: utf-8 -*-
"""
Array class for gaze coordinates.
"""

import numpy


class GazeArray(numpy.ndarray):
    """
    """
    
    def __new__(cls, input_array):
        """
        """
        
        obj = numpy.asarray(input_array).view(cls)
        
        return obj
    
    def __array_finalize__(self, obj):
        
        return


if __name__ == '__main__':
    
    from os import path
    
    data_filename = 'example.csv'
    root_path = path.dirname(path.dirname(path.abspath(__file__)))
    data_path = path.join(root_path, 'tests', 'data', data_filename)
    
    coords = numpy.genfromtxt(data_path, delimiter=',')
    
    gazedata = GazeArray(coords)
