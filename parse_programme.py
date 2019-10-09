IGNORE_DISCIPLINE = ("TEMP", "HULB")
BASE_URL = "https://www.ulb.be/api/formation"

params = {
    'path': '/ws/ksup/programme?anet={}&lang=fr'.format("BA-INFO"),
}

r = requests.get(BASE_URL, params=params)
data = json.loads(r.json()['json'])

name = data['blocs'][0]['anetTitle']

blocs = [x for x in data['blocs'] if x['level'] != 'P']

for bloc in blocs:
    bloc_name = "Bloc %s" % bloc['level']
    all_courses = [x for x in bloc['progCourses'] if not x['discipline'] in IGNORE_DISCIPLINE]
    mandataory_courses = [x for x in all_courses if x['mandatory']]
    options_courses = [x for x in all_courses if not x['mandatory']]
