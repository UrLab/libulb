from libulb import Client
from math import sqrt
from itertools import chain
import config

class options:
    color = True
    red = 10
    green = 12
    sepcolumns = "-+-"
    seplines = "-"
    columns = " | "

def colorize_text(color, text):
    if not options.color:
        return text
    return "\033[%dm%s\033[0m" % (color, text)

red = lambda txt: colorize_text(31, txt)
green = lambda txt: colorize_text(32, txt)
yellow = lambda txt: colorize_text(33, txt)
blue = lambda txt: colorize_text(34, txt)
magenta = lambda txt: colorize_text(35, txt)
hilight = lambda txt: colorize_text(1, txt)

def colorize_note(note):
    if note is None:
        return '----'
    n = round(note, 1)
    formatted = "%4s" % n
    if n < options.red:
        return red(formatted)
    elif n < options.green:
        return yellow(formatted)
    else:
        return green(formatted)

def bar(note):
    if note is None:
        res = '.' * 20
    else:
        res = red('*'*min(int(note), options.red)) +\
              yellow('*'*min(max(0, int(round(note-options.red))), options.green-options.red)) +\
              green('*'*min(max(0, int(round(note-options.green))), 20-options.green)) +\
              ' '*int(round(20-note))
    return res

def format_course(course):
    note = course.get('quality_points', None)
    ects_txt = blue("%2d" % int(course['credits']))
    return options.columns.join((
            hilight(yellow(course['mnemonique'])) if note is not None else course['mnemonique'], 
            colorize_note(note), 
            hilight(ects_txt) if note is not None and note >= options.red else ects_txt,
            bar(note),
            course['course_title']))

def main():
    session = Client.auth(config.NETID, config.PASSWD)
    inscriptions = filter(lambda inscr: inscr['term_code'] == '201415', session.inscriptions())
    all_notes = [x for inscr in inscriptions for x in session.notes(inscr)]
    notes = filter(lambda x: 'quality_points' in x, all_notes)
    ects = int(sum(x['credits'] for x in notes))

    mu = sum(x['quality_points']*x['credits'] for x in notes)/ects
    sigma = sqrt(sum(x['credits']*(x['quality_points']-mu)**2 for x in notes)/(ects-1))
    dev = 2.53*sigma/sqrt(ects-1)

    favgmin, favgmax = round(mu-dev, 1), round(mu+dev, 1)
    avgmin, avgmax = int(favgmin), int(favgmax)

    firstline = options.columns.join(map(hilight, (
        "Mnemonique", "Note", "Cr", "Histogramme".ljust(20), "Nom du cours")))

    lines = map(format_course, all_notes)
    avgline = options.columns.join((
        "Moyenne".rjust(10), 
        colorize_note(mu),
        magenta("%2d" % ects),
        ' '*avgmin + '*'*(avgmax-avgmin) + ' '*(20-avgmax),
        "99%% de chance que la moyenne soit entre %s et %s" % (
            colorize_note(favgmin), colorize_note(favgmax))))

    s = options.seplines
    separator = options.sepcolumns.join((s*10, s*4, s*2, s*20, s*52))

    all_ects = sum(x['credits'] for x in all_notes)
    supositions = []

    for i in [0, 12, 16]:
        mu = sum(map(lambda x: x['quality_points']*x['credits'] if 'quality_points' in x else i*x['credits'], all_notes))/all_ects
        supositions.append(options.columns.join((
            ("Si %d"%i).rjust(10), colorize_note(mu), magenta("%2d"%all_ects), bar(mu), 
            "Note finale si %d a tous les prochains examens" % i)))

    print
    print '\n'.join(chain([firstline, separator], lines, [separator, avgline], supositions))

if __name__ == "__main__":
    main()
