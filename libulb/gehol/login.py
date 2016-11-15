import requests


def login(netid, password):
    s = requests.session()

    data = {
        "_prtm": "login",
        "_prt": "ulb:gehol",
        "_ssl": "on",
        "_appl": "https://gehol.ulb.ac.be/gehol/intranet_login.php/",
        "_lang": "fr",
        "_username": netid,
        "_password": password,
        "_login": "login",
    }

    r = s.post('https://www.ulb.ac.be/commons/intranet', data=data)

    if not r.url == "https://gehol.ulb.ac.be/gehol/Vue/MonHoraire.php":
        raise Exception("Login failed")

    return s
