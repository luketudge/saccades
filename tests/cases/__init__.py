# -*- coding: utf-8 -*-
"""Dictionaries defining test cases.

Each dictionary defines a group of interchangeable cases.
The keys are used as the IDs displayed in the pytest output.
The values are further dictionaries with keys 'in' and 'out'.
'in' contains data going in to the test,
for example arrays, filenames, function arguments, etc.
'out' contains expected results,
for example transformed arrays, expected exceptions, etc.
The 'out' key may be absent if no particular output is expected,
for example if we are just testing that no exception is raised,
or if the output is always the same for all cases.

In each module, the UPPERCASE names represent the test cases.
These are parametrized into test fixtures in conftest.py.
"""
