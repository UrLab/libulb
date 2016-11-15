libulb
======

Python lib for ULB (ulb.ac.be)

libulb is Python3 only.

Install
=======

::

    pip install git+https://github.com/C4ptainCrunch/libulb.git

Example
=======

::

    # -*- coding: utf-8 -*-
    from __future__ import print_function, unicode_literals

    from libulb.smileye_app import api
    from datetime import datetime

    c = api.Client.auth('adelcha', 'pAssW0r!')

    info = c.info()
    print(info['name']) # Alain

    inscriptions = c.inscriptions()
    notes_first_year = c.notes(inscriptions[0])

    c.note_detail(c.notes(c.inscriptions()[-1])[-1]) # Details of the last course of your last year

    c.gehol(datetime(2015, 5, 5, 0, 0, 0), datetime(2015, 5, 6, 0, 0, 0)) # All of your courses of the day

Dev
===

``git clone`` then ``pip install -e .`` and
``pip install -r requirements-dev.txt``
