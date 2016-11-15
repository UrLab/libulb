#!/usr/bin/env python
# coding: utf-8

from libulb.smileye_app.api import Client
from datetime import datetime
import config
import json


class Options:
    color = True
    red = 10
    green = 12
    sepcolumns = "-+-"
    seplines = "-"
    columns = " | "


def colorize_text(color, text):
    if not Options.color:
        return text
    return "\033[%dm%s\033[0m" % (color, text)

red = lambda txt: colorize_text(31, txt)
green = lambda txt: colorize_text(32, txt)
yellow = lambda txt: colorize_text(33, txt)
blue = lambda txt: colorize_text(34, txt)
magenta = lambda txt: colorize_text(35, txt)
hilight = lambda txt: colorize_text(1, txt)


class Course:
    separator = Options.sepcolumns.join((
        Options.seplines*10, Options.seplines*4, Options.seplines*2,
        Options.seplines*20, Options.seplines*52))

    @classmethod
    def titles(cls):
        return Options.columns.join(map(hilight, (
            "Mnemonique", "Note", "Cr", "Histogramme".ljust(20), "Nom du cours")))

    def __init__(self, mnemonic, name, ects, note=None, lower_note=0, upper_note=None):
        self.mnemonic = mnemonic
        self.name = name
        self.ects = ects
        self.note = note
        self.lower_note = lower_note
        self.upper_note = note if upper_note is None else upper_note

    def __unicode__(self):
        return Options.columns.join((
            self.colorize_mnemonic(),
            self.colorize_note(),
            self.colorize_ects(),
            self.bar(),
            self.name))

    @classmethod
    def from_ulb_api(cls, api_dict):
        return cls(
            mnemonic=api_dict['mnemonique'],
            name=api_dict['course_title'],
            ects=int(api_dict['credits']),
            note=api_dict.get('quality_points', None))

    def default_note(self, note):
        return note if self.note is None else self.note

    ### FORMATTERS ###
    def colorize_mnemonic(self):
        as_str = self.mnemonic.rjust(10)
        if self.note is not None:
            return hilight(yellow(as_str))
        return as_str

    def colorize_note(self):
        if self.note is None:
            return '----'
        n = round(self.note, 1)
        formatted = "%4s" % n
        if n < Options.red:
            return red(formatted)
        elif n < Options.green:
            return yellow(formatted)
        else:
            return green(formatted)

    def colorize_ects(self):
        as_str = "%2d" % int(self.ects)
        if self.note is not None:
            if self.note < 10:
                return red(as_str)
            else:
                return green(as_str)
        return blue(as_str)

    def bar(self):
        if self.note is None:
            return '.'*20

        lower, upper = int(round(self.lower_note)), int(round(self.upper_note))
        if lower > 0:
            lower -= 1

        res = ' '*int(round(lower))
        for i in range((lower), (upper)):
            cur = hilight('*') if i+1 == round(self.note) else '*'

            if i+1 < Options.red:
                res += red(cur)
            elif i+1 < Options.green:
                res += yellow(cur)
            else:
                res += green(cur)

        res += ' '*(20-int(round(upper)))
        return res


def print_notes(api_client, inscription):
    courses = map(Course.from_ulb_api, api_client.notes(inscription))
    passed = inscription.get('grade_annee_reussite', None)
    if passed == 'Y':
        passed_string = green(inscription['grade_annee_desc'])
    elif passed == 'N':
        passed_string = red(inscription['grade_annee_desc'])
    else:
        passed_string = u"en cours"

    for c in courses:
        if c.mnemonic in know.keys():
            c.note = know[c.mnemonic]
            c.upper_note = know[c.mnemonic]


    print hilight("%s - %s (session %d) - %s" % (
        inscription['area'], inscription['term_desc'],
        inscription['session_num'], passed_string))
    print Course.titles()
    print Course.separator
    print '\n'.join(map(unicode, courses))

    evaluated = filter(lambda c: c.note is not None, courses)
    if evaluated:
        ects = sum(x.ects for x in evaluated)
        mu = sum(x.note*x.ects for x in evaluated)/ects
        all_ects = sum(x.ects for x in courses)
        all_0 = round(sum(c.default_note(0)*c.ects for c in courses)/all_ects, 1)
        all_20 = round(sum(c.default_note(20)*c.ects for c in courses)/all_ects, 1)
        description = "Note finale"
        if all_ects != ects:
            description += " entre %s et %s" % (str(all_0), str(all_20))
        avg_course = Course(
            mnemonic="Moyenne",
            name=description,
            ects=ects, note=mu,
            lower_note=all_0,
            upper_note=all_20)
        if evaluated == courses:
            print hilight(blue(Course.separator))
        else:
            print Course.separator
        print unicode(avg_course)

    passed = filter(lambda c: c.note and c.note >= 10, courses)
    if passed:
        ects = sum(x.ects for x in passed)
        mu = sum(x.note*x.ects for x in passed)/ects
        avg_course = Course(
            mnemonic="Reussis",
            name="Cours dont la note est >= 10/20",
            ects=ects, note=mu, lower_note=mu)
        print unicode(avg_course)

    print


def main(netid, passwd, exam_session=None, year=None):
    if year is None:
        year = datetime.now().year if datetime.now().month >= 10 else datetime.now().year-1
    this_year_str = '%d%d' % (year, (year+1) % 100)

    this_year = lambda inscr: inscr['term_code'] == this_year_str
    condition = this_year
    if exam_session is not None:
        this_session = lambda inscr: inscr['session_num'] == exam_session
        condition = lambda inscr: this_year(inscr) and this_session(inscr)

    session = Client.auth(netid, passwd)
    for inscr in filter(condition, session.inscriptions()):
        print_notes(session, inscr)

if __name__ == "__main__":
    import argparse
    from getpass import getpass

    optparser = argparse.ArgumentParser(description=u"Points des cours à l'ULB")
    optparser.add_argument(
        "--netid", "-n", action='store',
        type=str, dest='netid', default=config.NETID,
        help=u"Affiche les points pour ce netid ('%s' par defaut)" % (config.NETID))
    optparser.add_argument(
        "--no-color", "-C", action='store_false',
        dest='color', default=True,
        help=u"N'affiche pas les résultats en couleur")
    optparser.add_argument(
        "-s", "--session", action='store',
        type=int, dest='session', default=None,
        help=u"Affiche les points de cette session uniquement")
    optparser.add_argument(
        "-y", "--year", action='store',
        type=int, dest='year', default=None,
        help=u"Année à afficher (année du premier quadrimestre)")
    optparser.add_argument(
            "--know", "-k",
            dest='know', type=json.loads,
            help=u"Cours dont la note est connue en json (ex: '{\"INFO-F-308\": 18, \"INFO-F-309\":15}')"
            )
    clargs = optparser.parse_args()

    Options.color = clargs.color
    while not clargs.netid:
        clargs.netid = raw_input("NetID ? ")

    passwd = "" if clargs.netid != config.NETID else config.PASSWD
    while not passwd:
        passwd = getpass()

    know = clargs.know if clargs.know is not None else {}

    main(clargs.netid, passwd, clargs.session, clargs.year)
