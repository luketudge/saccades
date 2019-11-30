# -*- coding: utf-8 -*-

import setuptools


setuptools.setup(
    name='saccades',
    version='0.1',
    description='Tools for analyzing saccades.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/luketudge/saccades',
    author='Luke Tudge',
    author_email='luketudge@gmail.com',
    classifiers=['Programming Language :: Python :: 3',
                 'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)'],
    packages=['saccades'],
    install_requires=['numpy', 'pandas'],
    python_requires='>=3'
)
