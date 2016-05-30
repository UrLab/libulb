import requests
from bs4 import BeautifulSoup
import re
import urllib

def get_session(netid, password):
    payload={
        "username": netid,
        "password": password,
    }

    s = requests.Session()
    s.post("https://uv.ulb.ac.be/login/index.php", data=payload)

    return s

def _chop_category(category):
    url = category.find('a')['href']
    split = urllib.parse.urlsplit(url)
    qs = urllib.parse.parse_qs(split.query)

    return {
        "url": url,
        "name": category.find('a').text,
        "id": int(qs["categoryid"][0])
    }

def _list_categories(s):
    categories_html = s.get("http://uv.ulb.ac.be/course/")
    soup = BeautifulSoup(categories_html.text, "html.parser")
    dropdowns = soup.findAll(class_="info")

    categories = [_chop_category(cat) for cat in dropdowns]
    return categories

def _chop_course(course):
    course_link = course.find(class_="coursename").find("a")
    mnemo = None
    m = re.match(r'(\w{4})-(\w)(\d{3,4})', course_link.text)
    if m:
        mnemo = ("%s-%s-%s" % m.groups()).lower()

    match = re.match(r'^(.*) - \d{4,8}$', course_link.text)
    if match:
        name = match.groups()[-1]
    else:
        name = course_link.text

    url = course_link['href']
    split = urllib.parse.urlsplit(url)
    qs = urllib.parse.parse_qs(split.query)

    name = re.match(r'^(\w{4}-\w\d{3,4})?( - )?(.*)$', name).groups()[-1].strip().replace("  ", "").replace("  ", " ")
    return {
        "mnemo": mnemo,
        "name": name,
        "url": url,
        "id": int(qs["id"][0]),
        "can_register": course.find(title="Auto-inscription") is not None,
    }

def _list_category_courses(s, category_id):
    # List courses of categories
    section = s.get("http://uv.ulb.ac.be/course/index.php?categoryid=%i&perpage=5000&browse=courses" % category_id)
    soup = BeautifulSoup(section.text, "html.parser")

    courses = [_chop_course(c) for c in soup.findAll(class_="coursebox")]
    return courses


def subscribe(s, course_id):
    course_page = s.get("http://uv.ulb.ac.be/course/view.php?id=%i" % course_id)
    if "enrol" in course_page.url:
        if "Clef d'inscription" in course_page.text:
            raise RuntimeError("This course needs a key, please enter it manualy")
        enrol_url = "http://uv.ulb.ac.be/enrol/index.php"
        soup = BeautifulSoup(course_page.text, "html.parser")
        form = soup.find("form", action=enrol_url)
        if form is None:
            if "Continuer" in course_page.text:
                raise RuntimeError("You can not subscribe to this course")
            else:
                raise RuntimeError("Unknown content on this page, please file a bugreport")
        fields = form.findAll('input')
        payload = {x['name']: x['value'] for x in fields}
        s.post(enrol_url, data=payload)
    else:
        raise RuntimeError("User was already subscribed")


def unsubscribe(s, course_id):
    course_page = s.get("http://uv.ulb.ac.be/course/view.php?id=%i" % course_id)
    if "enrol" not in course_page.url:
        soup = BeautifulSoup(course_page.text, "html.parser")
        has_unrol = lambda x: "http://uv.ulb.ac.be/enrol/self/unenrolself.php" in x['href']
        link = list(filter(has_unrol, soup.findAll("a")))[0]

        unrol_page = s.get(link['href'])
        unrol_url = "http://uv.ulb.ac.be/enrol/self/unenrolself.php"
        soup = BeautifulSoup(unrol_page.text, "html.parser")
        form = soup.find("form", action=unrol_url)
        fields = form.findAll('input')
        payload = {x.get('name',""): x['value'] for x in fields}
        s.post(unrol_url, data=payload)
    else:
        raise RuntimeError("User was already unsubscribed")


def is_subscribed(s, course_id):
    course_page = s.get("http://uv.ulb.ac.be/course/view.php?id=%i" % course_id)
    return "enrol" not in course_page.url


def list_courses(s):
    categories = _list_categories(s)
    courses = []

    for cat in categories:
        courses += _list_category_courses(s, cat['id'])

    return courses


def _is_file(a):
    url = a["href"]
    if url.startswith( "http://uv.ulb.ac.be/mod/resource/view.php?id="):
        return True
    if re.match(r'http://uv\.ulb\.ac\.be/pluginfile\.php/\d+/mod_folder/', url):
        return True

    return False

def _chop_file(a):
    name_tag = a.find(class_="fp-filename") or a.find(class_="instancename")
    url = furl(a['href'])
    url.args["forcedownload"] = 1
    url.args["redirect"] = 1

    name = name_tag.text.replace("_", " ")
    return {
        "name": name,
        "url": url.url,
    }

def _get_folder_files(s, url, name):
    page = s.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    tree = soup.find(class_="foldertree")
    files = [_chop_file(a) for a in tree.findAll("a")]
    for f in files:
        f['dirname'] = name
    return files

def extract_files_url(s, course_id):
    page = s.get("http://uv.ulb.ac.be/course/view.php?id=%i" % course_id)
    soup = BeautifulSoup(page.text, "html.parser")
    main = soup.find(id="region-main")

    links = main.findAll("a")
    is_folder = lambda x: x["href"].startswith("http://uv.ulb.ac.be/mod/folder/view.php?id=")
    chop_folder = lambda x: {
        'url': x['href'],
        'name': list(x.find(class_="instancename").strings)[0]
    }

    folders = [chop_folder(a) for a in filter(is_folder, links)]
    files = [_chop_file(a) for a in filter(_is_file, links)]

    folder_files = [_get_folder_files(s, f["url"], f["name"]) for f in folders]

    return files + folder_files


def search_course(s, mnemo):
    match = re.match(r"(\w{3,4})-(\w)-(\d{3,4})", mnemo.lower())
    if not match:
        raise ValueError("The mnemonic must be in the form 'info-f-303 or info-f-1001'")
    mnemo = "%s-%s%s" % match.groups()

    page = s.get("http://uv.ulb.ac.be/course/search.php?search=%s" % mnemo)
    soup = BeautifulSoup(page.text, "html.parser")

    results = soup.find(class_="course-search-result-search")
    if not results:
        return None
    divs = results.findAll(class_="info")

    if len(divs) == 0:
        return None
    else:
        d = divs[-1]

    return _chop_course(d)
