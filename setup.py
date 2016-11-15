# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='libulb',
    version='0.1',
    description='Interact with ULB in python',
    url='https://github.com/C4ptainCrunch/libulb',
    author='Nikita Marchant',
    author_email='nikita.marchant@ulb.ac.be',
    license='BSD',
    zip_safe=False,
    install_requires=[
        'requests',
        'BeautifulSoup4',
        'six',
        'PyYaml',
        'html5lib',
        'furl',
    ],
    entry_points={
        'console_scripts': [
            'make-course-tree=libulb.catalog.extractor:main',
            'mes-notes-ulb=libulb.smileye_app.mesnotes:command',
        ],
    }
)
