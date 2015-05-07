import requests
import json


class Client:

    BASE = "https://smileyee-api-prd.ulb.ac.be:8443/ws/"

    def __init__(self, pidm, token):
        self.pidm = pidm
        self.token = token

        self._get_user_info()

    @classmethod
    def auth(cls, netid, password):
        params = {
            'username': netid,
            'password': password,
            'pwdEncrypted=': 'false',
            'sendEncryptedPwd': 'false',
        }
        resp = requests.get(cls.BASE + "Login", params=params)
        user = json.loads(resp.text[5:-2])
        pidm = user['data'][0]['pidm']
        token = user['token']

        return cls(pidm, token)

    def _get_user_info(self):
        params = {'token': self.token}
        resp = requests.get(self.BASE + "rest/etudiants/" + str(self.pidm), params=params)
        j = resp.json()
        data = j['data'][0]

        self.matricule = data['banner_id']
        self.name = data['prenom']
        self.surname = data['nom']
        self.sex = data['sexe']
        self.civilite = data['civilite']
        self.birth = data['date_naissance_desc']
        self.birth_place = data['lieu_naissance']
        self.birth_country = data['pays_naissance_desc']
        self.nationality = data['nationalite']
        self.etat_civil = data['etat_civil_desc']
        self.bibilo_id = data['bibliocode']
        self.private_email = data['emailpri']
        self.ulb_email = data['emailulb']
        self.address = {
            'street': data['addresse1_pr'],
            'postal_code': data['code_postal_pr'],
            'locality': data['localite_pr'],
            'country': data['pays_desc_pr'],
        }
        self.phone = data['telephone']

    def inscriptions(self):
        params = {'token': self.token}
        resp = requests.get(self.BASE + "rest/etudiants/" + str(self.pidm) + "/inscriptions", params=params)
        data = resp.json()['data']

        return data

    def notes(self, inscription):
        session = inscription['session_num']
        dgmr_seq_no = inscription['dgmr_seq_no']
        params = {
            'token': self.token,
            'session': session,
        }
        resp = requests.get(
            self.BASE + "rest/etudiants/" + str(self.pidm) + "/inscriptions/" + str(dgmr_seq_no) + "/notes",
            params=params
        )
        data = resp.json()['data']

        return data
