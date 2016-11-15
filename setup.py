# -*- coding: utf-8 -*-

from setuptools import setup

with open("README.rst", 'r') as fd:
    readme = fd.read()

setup(
    name='libulb',
    version='0.1.3',
    description='Interact with ULB in python',
    url='https://github.com/C4ptainCrunch/libulb',
    author='Nikita Marchant',
    author_email='nikita.marchant@ulb.ac.be',
    license='BSD',
    zip_safe=False,
    packages=['libulb'],
    include_package_data=True,
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
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',

    ],
    long_description=readme,
)
