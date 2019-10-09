URL = "https://www.ulb.be/servlet/search?beanKey=beanKeyRechercheFormation&&natureFormation=ulb&s=FACULTE_ASC&limit=1000"
r = requests.get(URL)
soup = BeautifulSoup(r.text)

REJECT = [
    "Certificat d'aptitude",
    "Agrégation",
    "décalé",
]

PREFIXES = [
    "Master de ",
    "Master en ",
    "Bachelier en ",
    "Master : ",
    "Spécialisation en",
    "Sciences de la "
]

items = soup.findAll(class_="search-result__result-item")

def stripmany(s, to_strip):
    ret = s
    for prefix in to_strip:
        if ret.startswith(prefix):
            ret = ret[len(prefix):]
    return ret

def extract(item):
    name = item.find(class_="search-result__structure-intitule").text.replace("  ", " ").strip(" ")
    name = unicodedata.normalize("NFC", name)
    small_name = stripmany(name, PREFIXES).strip(" ")
    small_name = small_name.capitalize()

    return {
        "name": name,
        "fac": item.find(class_="search-result__structure-rattachement").text,
        "slug": item.find(class_="search-result__mnemonique").text,
        "small-name": small_name,
        "master": True if "Master" in name else False
    }

def contains_many(where, what):
    for s in what:
        if s in where:
            return True
    return False

def make_unique(l):
    seen = set()
    out = []
    for x in l:
        if x['slug'] not in seen:
            seen.add(x['slug'])
            out.append(x)
    return out

program_list = [extract(x) for x in items]
filtered_programs = make_unique([x for x in program_list if not contains_many(x['name'], REJECT)])

base_tree = defaultdict(lambda: {'bachelor': [], 'master': []})

for program in filtered_programs:
    fac = program['fac']
    t = 'master' if program['master'] else 'bachelor'
    base_tree[fac][t].append(program)


for i in filtered_programs:
    print(i['small-name'])
