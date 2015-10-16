import requests
import re
import json
from libulb.tools import Slug


def get_list():
    txt = requests.get("http://gehol.ulb.ac.be/gehol/Vue/HoraireCours.php").text
    courses = json.loads(re.search(r'<script>\s\n\svar data =(.*);\s\n', txt).groups()[0])

    ret = {}

    for course in courses:
        mnemo = course['label']
        name = course['value']

        name = name.replace("[{}]".format(mnemo), "").strip()
        slug = Slug.from_gehol(mnemo)

        ret[slug] = name

    return ret
