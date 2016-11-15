# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='libulb',
    version='0.1.dev',
    description='Interact with ULB in python',
    url='https://github.com/C4ptainCrunch/libulb',
    author='Nikita Marchant',
    author_email='nikita.marchant@ulb.ac.be',
    license='BSD',
    packages=find_packages(exclude="[examples]"),
    zip_safe=False,
    install_requires=[
        'requests',
        'BeautifulSoup4',
        'six',
        'PyYaml',
        'html5lib',
        'furl',
    ],
)
