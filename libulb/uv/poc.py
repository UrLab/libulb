import requests
from bs4 import
import re

s = requests.Session()
s.post("https://uv.ulb.ac.be/login/index.php", data=payload)

categories_html = s.get("http://uv.ulb.ac.be/course/")
soup = BeautifulSoup(categories_html.text, "html.parser")
dropdowns = soup.findAll(class_="info")

categories = [(cat.find('a')['href'], cat.find('a').text) for cat in dropdowns]


section = s.get("http://uv.ulb.ac.be/course/index.php?categoryid=68&perpage=5000&browse=courses")
soup = BeautifulSoup(section.text, "html.parser")


def chop_course(course):
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

    name = re.match(r'^(\w{4}-\w\d{3,4})?( - )?(.*)$', name).groups()[-1].strip().replace("  ", "").replace("  ", " ")
    return {
        "mnemo": mnemo,
        "name": name,
        "url": course_link['href'],
        "can_register": course.find(title="Auto-inscription") is not None,
    }


courses = [chop_course(c) for c in soup.findAll(class_="coursebox")]


course_page = s.get("http://uv.ulb.ac.be/course/view.php?id=51823")
if "enrol" in course_page.url:
    enrol_url = "http://uv.ulb.ac.be/enrol/index.php"
    soup = BeautifulSoup(course_page.text, "html.parser")
    form = soup.find("form", action=enrol_url)
    fields = form.findAll('input')
    payload = {x['name']: x['value'] for x in fields}
    s.post(enrol_url, data=payload)
else:
    print("Alredy subscribed")


course_page = s.get("http://uv.ulb.ac.be/course/view.php?id=51823")
if "enrol" not in course_page.url:
    soup = BeautifulSoup(course_page.text, "html.parser")
    form = soup.find("form", action=enrol_url)
    fields = form.findAll('input')
    payload = {x['name']: x['value'] for x in fields}
    s.post(enrol_url, data=payload)
else:
    print("Alredy unsubscribed")
