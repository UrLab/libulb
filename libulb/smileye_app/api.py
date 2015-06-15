# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

import requests
import json


class Client:

    BASE = "https://smileyee-api-prd.ulb.ac.be:8443/ws/"

    def __init__(self, pidm, token):
        self.pidm = pidm
        self.token = token

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

    def info(self):
        params = {'token': self.token}
        resp = requests.get(self.BASE + "rest/etudiants/" + str(self.pidm), params=params)
        j = resp.json()
        data = j['data'][0]

        info = {
            'matricule': data['banner_id'],
            'name': data['prenom'],
            'surname': data['nom'],
            'sex': data['sexe'],
            'title': data['civilite'],
            'birth': data['date_naissance_desc'],
            'birth_place': data['lieu_naissance'],
            'birth_country': data['pays_naissance_desc'],
            'nationality': data['nationalite'],
            'vital_record': data['etat_civil_desc'],
            'biblio_id': data['bibliocode'],
            'private_email': data['emailpri'],
            'ulb_email': data['emailulb'],
            'address': {
                'street': data['addresse1_pr'],
                'postal_code': data['code_postal_pr'],
                'locality': data['localite_pr'],
                'country': data['pays_desc_pr'],
            },
            'phone': data['telephone'],
        }

        return info

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

    def note_detail(self, note):
        session = note['session_num']
        dgmr_seq_no = note['dgmr_seq_no']
        crn = note['crn']
        params = {
            'token': self.token,
            'session': session,
        }
        resp = requests.get(
            self.BASE + "rest/etudiants/" + str(self.pidm) + "/inscriptions/" + str(dgmr_seq_no) + "/notes/" + str(crn),
            params=params
        )

        return resp.json()['data'][0]

    def photo(self):
        """Returns bytes containing a .jpg image of the student"""

        params = {'token': self.token}
        resp = requests.get(self.BASE + "rest/etudiants/" + str(self.pidm) + "/photo", params=params)

        return resp.content

    def gehol(self, start, stop):
        """Returns a list of courses that have an intersection with the timespan given by start and stop.
        Both should be naive datetime.datetime objects in the Belgian timezone"""

        form = "%Y-%m-%dT%H:%M:%S.000Z"
        params = {
            'token': self.token,
            'startDate': start.strftime(form),
            'endDate': stop.strftime(form),
        }
        resp = requests.get(self.BASE + "rest/etudiants/" + str(self.pidm) + "/horaire", params=params)

        return resp.json()['data']

    def announces(self):
        params = {'token': self.token}
        resp = requests.get(self.BASE + "rest/etudiants/" + str(self.pidm) + "/annonces", params=params)

        return resp.json()['data']

    def announce_detail(self, announce):
        params = {'token': self.token}
        taid = announce['taid']
        resp = requests.get(self.BASE + "rest/etudiants/" + str(self.pidm) + "/annonces/" + str(taid), params=params)

        return resp.json()['data'][0]
