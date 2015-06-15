import requests
from bs4 import BeautifulSoup

def _get_course(year, fac, num):
    url = "http://banssbfr.ulb.ac.be/PROD_frFR/bzscrse.p_disp_course_detail"
    params = {
        'cat_term_in': year,
        'subj_code_in': fac,
        'crse_numb_in': num,
    }
    return requests.get(url, params=params)

def _course_to_dict(html):
    soup = BeautifulSoup(html)

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

    return infos


def _dict_to_course(d):
    name = d["Intitulé de l'unité d'enseignement"]

    language = d.get("Langue d'enseignement", None)
    if "français" in language:
        language = "french"
    elif "anglais" in language:
        language = "english"
    else:
        if "Enseigné en" in language:
            language = language.replace("Enseigné en", "")
        else:
            language = None

    profs = []
    prof_str = d.get("Titulaire(s)", None)
    if not (prof_str is None or prof_str.strip() == ""):
        for prof in prof_str.split(','):
            prof = prof.replace("(coordonnateur)", "")
            prof = prof.strip()
            prof = prof.title()
            profs.append(prof)

    requirements = d.get("Connaissances et compétences pré-requises", None)

    sections = []
    sections_str = d.get("Programme d'études comprenant l'unité d'enseignement", None)
    if sections_str is not None and sections_str.strip() != "":
        for section in sections_str.split("\n"):
            match_section = re.match(r'^- ([A-Z1-9\-]{2,}) -', section)
            if match_section:
                search = re.search(r'\(([0-9]+) (crédit|crédits), (optionnel|obligatoire)\)', section)
                sections.append({
                    'section': match_section.group(1),
                    'credits': int(search.group(1)),
                    'required': search.group(3) == 'obligatoire'
                })







a = _get_course("201516", "INFO", "F101")
d = _parse_course(a.text)
