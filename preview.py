import requests
import json

REST = "https://smileyee-api-prd.ulb.ac.be:8443/ws"

resp = requests.get(
    REST +"/Login?username={username}&password={passw}&pwdEncrypted=false&sendEncryptedPwd=false".format(
        username="nimarcha",
        passw=passw
    )
)
user = json.loads(resp.text[5:-2])
pidm = user['data'][0]['pidm']
token = user['token']



resp = requests.get(REST + "/rest/etudiants/{pidm}/inscriptions?token={token}".format(
    token=token,
    pidm=pidm,
))

j = resp.json()
inscription = j['data'][-2]

resp = requests.get(REST + "/rest/etudiants/162596/inscriptions/{dgmr_seq_no}/notes?session={session_num}&token={token}".format(
    token=token,
    pidm=pidm,
    dgmr_seq_no=inscription['dgmr_seq_no'],
    session_num=inscription['session_num']
))

