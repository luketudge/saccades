# -*- coding: utf-8 -*-
"""Regular expressions for reading eyetracking data files.
"""

import regex


FLAGS = regex.V1


# %% Row format

POS_INTEGER = r'\d+'
"""1 or more digits.
"""

INTEGER = '-?' + POS_INTEGER
"""Optionally a minus sign, \
then INTEGER.
"""

FLOAT = r'-?\d*\.\d*'
"""Optionally a minus sign, \
then 0 or more digits, \
then a dot, \
then 0 or more digits.
"""

NUMBER = '({}|{})'.format(INTEGER, FLOAT)
"""INTEGER or FLOAT.
"""

FILLER = '.*'
"""0 or more occurrences of any character.
"""
