# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

from setuptools import setup

setup(
    name='libulb',
    version='0.1.dev',
    description='Interact with ULB in python',
    url='https://github.com/C4ptainCrunch/libulb',
    author='Nikita Marchant',
    author_email='nikita.marchant@ulb.ac.be',
    license='BSD',
    packages=['libulb'],
    zip_safe=False,
    install_requires=[
        'requests',
        'BeautifulSoup4',
        'six',
    ],
)
