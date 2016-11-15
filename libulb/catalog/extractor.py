#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import yaml
import requests
from bs4 import BeautifulSoup
import sys


def handle_node(node):
    name = getattr(node, "name", None)

    if name is None:  # we have text, not a tag
        txt = node.strip()
        mnemo = re.search(r'([A-Z]{4}-[A-Z])([0-9]{3,4})', txt)
        if mnemo:
            return (mnemo.group(1) + '-' + mnemo.group(2)).lower()

        cours_obligatoire = re.search(r'Cours obligatoires - (.*)', txt)
        if cours_obligatoire:
            return cours_obligatoire.group(1).strip()

        cours_options = re.search(r'Cours à (options|choisir) - (.*)', txt)
        if cours_options:
            return cours_options.group(1).strip()

        choisir_parmis = re.search(r'Choisir [0-9]+ ECTS parmi les cours suivants', txt)
        if choisir_parmis:
            return ""

        return txt

    children = []
    for child in node.children:
        child = handle_node(child)
        if isinstance(child, list):
            if len(child) > 0 and isinstance(child[0], list):
                children.extend(child)
            elif child:
                children.append(child)
        elif child:
            children.append(child)

    while len(children) == 1:
        children = children[0]

    return children

URL = "http://banssbfr.ulb.ac.be/PROD_frFR/bzscrse.p_disp_prog_detail?term_in={}&prog_in={}&lang=FRENCH"


def get_approximate_tree(section_slug, year="201617"):
    url = URL.format(year, section_slug)
    r = requests.get(url)

    soup = BeautifulSoup(r.text, "html5lib")
    body = soup.find('div', class_="pagebodydiv")
    tables = filter(lambda x: x.name == "table" and x['class'] == ['progcattable'], body.contents)

    output = []
    for table in tables:
        data = handle_node(table)
        output.extend(data)

    return output


def main():
    if len(sys.argv) not in (2, 3):
        print("Usage: %s section-slug [year]\nExample: %s ba-info 201617" % (sys.argv[0], sys.argv[0]))
        exit(-1)
    section = sys.argv[1]

    if len(sys.argv) == 3:
        year = sys.argv[2]
        tree = get_approximate_tree(section, year)
    else:
        tree = get_approximate_tree(section)

    if len(tree) == 0:
        print("No courses found for section '%s'" % section)
        exit(-1)

    print(yaml.safe_dump(
        tree,
        default_flow_style=False,
        width=500,
        indent=4,
        allow_unicode=True
    ))
