import libulb

c = libulb.Client.auth('adelcha', 'pAssW0r!')

info = c.info()
print(info['name']) # Alain

inscriptions = c.inscriptions()
notes_first_year = c.notes(inscriptions[0])
