# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

import requests
from bs4 import BeautifulSoup
import re


class Course:
    def __init__(self, slug, year, infos):
        self.slug = slug
        self.year = year

        self._fill(infos)

    def __repr__(self):
        if self.credits:
            return "<Course {}: {} ({} crédits)>".format(self.slug, self.name, self.credits)
        else:
            return "<Course {}: {}>".format(self.slug, self.name)

    @classmethod
    def get_from_slug(cls, slug, year):
        slug = slug.upper()
        match = re.match(r'([A-Z]{4})-?([A-Z])-?([0-9]{2,4})', slug)
        if not match:
            raise ValueError("Invalid slug format")

        response = cls._query_ulb(year, match.group(1), match.group(2) + match.group(3))
        if not response.ok:
            raise Exception("Error with ulb")

        soup = BeautifulSoup(response.text)

        table = soup.find('table', 'bordertable')
        tr_list = table('tr')

        infos = {}

        for line in tr_list:
            if len(line('td')) != 2:
                continue
            key, val = line('td')
            key = key.text.strip().strip("*").strip()
            val = val.text.strip().strip("*").strip()
            infos[key] = val

        slug = "{}-{}-{}".format(match.group(1), match.group(2), match.group(3)).lower()
        return cls(slug, year, infos)

    @classmethod
    def _query_ulb(cls, year, fac, num):
        url = "http://banssbfr.ulb.ac.be/PROD_frFR/bzscrse.p_disp_course_detail"
        params = {
            'cat_term_in': year,
            'subj_code_in': fac,
            'crse_numb_in': num,
        }
        return requests.get(url, params=params)

    def _fill(self, d):
        self.name = d["Intitulé de l'unité d'enseignement"]

        language = d.get("Langue d'enseignement", None)
        if "français" in language:
            self.language = "french"
        elif "anglais" in language:
            self.language = "english"
        elif "néerlandais" in language:
            self.language = "dutch"
        else:
            if "Enseigné en" in language:
                self.language = language.replace("Enseigné en", "").strip()
            else:
                self.language = None

        self.profs = []
        prof_str = d.get("Titulaire(s) * [y inclus le coordonnateur]", None)
        if not (prof_str is None or prof_str.strip() == ""):
            for prof in prof_str.split(','):
                prof = prof.replace("(coordonnateur)", "")
                prof = prof.strip()
                prof = prof.title()
                self.profs.append(prof)

        self.requirements = d.get("Connaissances et compétences pré-requises", None)

        self.sections = []
        sections_str = d.get("Programme(s) d'études comprenant l'unité d'enseignement", None)
        # import ipdb; ipdb.set_trace()
        if sections_str is not None and sections_str.strip() != "":
            for section in sections_str.split("\n"):
                match_section = re.match(r'^- ([A-Z1-9\-]{2,}) -', section.strip())
                if match_section:
                    search = re.search(r'\(([0-9]+) (crédit|crédits), (optionnel|obligatoire)\)', section)
                    self.sections.append({
                        'section': match_section.group(1),
                        'credits': int(search.group(1)),
                        'required': search.group(3) == 'obligatoire'
                    })

        if len(self.sections) != 0:
            self.credits = max(map(lambda x: x['credits'], self.sections))
        else:
            self.credits = None

if __name__ == '__main__':
    course = Course.get_from_slug('info-f-101', "201516")
