#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import yaml
import requests
from bs4 import BeautifulSoup
import sys

URL = "http://banssbfr.ulb.ac.be/PROD_frFR/bzscrse.p_disp_prog_detail?term_in=201516&prog_in={}&lang=FRENCH"


def handle_node(node):
    name = getattr(node, "name", None)

    if name is None: # we have text, not a tag
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
        if child:
            children.append(child)

    while len(children) == 1:
        children = children[0]

    return children

if __name__ == '__main__':
    section = sys.argv[1]
    url = URL.format(section)
    r = requests.get(url)

    soup = BeautifulSoup(r.text, "html5lib")
    body = soup.find('div', class_="pagebodydiv")
    tables = filter(lambda x: x.name == "table" and x['class'] == ['progcattable'], body.contents)

    output = []
    for table in tables:
        data = handle_node(table)
        output.append(data)

    print(yaml.safe_dump(
        output,
        default_flow_style=False,
        width=500,
        indent=4,
        allow_unicode=True
    ))
