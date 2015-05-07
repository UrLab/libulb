import libulb
from datetime import datetime

c = libulb.Client.auth('adelcha', 'pAssW0r!')

info = c.info()
print(info['name']) # Alain

inscriptions = c.inscriptions()
notes_first_year = c.notes(inscriptions[0])

c.note_detail(c.notes(c.inscriptions()[-1])[-1]) # Details of the last course of your last year

c.gehol(datetime(2015, 05, 05, 0, 0, 0), datetime(2015, 05, 06, 0, 0, 0)) # All of your courses of the day

