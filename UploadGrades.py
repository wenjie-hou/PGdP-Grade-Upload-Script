# coding=utf-8


import datetime
import json
import requests


#load config from config.json
config = json.loads(open("config.json", "r").read())

exercisesID = config['exerciseID']
courseid = config['courseID']
username = config['username']
password = config['password']

headers = {
  'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36",
  'X-XSRF-TOKEN': "2d141b5-9e1c-4390-ae06-5143753b4459",
  'Content-Type': "application/json;charset=UTF-8",
  'Accept': "application/json, text/plain, */*"
}

cookies = {'XSRF-TOKEN': "2d141b5-9e1c-4390-ae06-5143753b4459"}

def authenticate():
  urlAuth = 'https://artemis.ase.in.tum.de/api/authenticate'
  payload = '{{"username": "{}", "password": "{}", "rememberMe": false}}'.format(username, password)
  res = requests.post(urlAuth, data=payload, headers=headers, cookies=cookies)
  headers.update({"Authorization": "{}".format(res.headers['Authorization'])})

def manualResult():
  baseUrl = 'https://artemis.ase.in.tum.de/api/manual-results'
  with open('result.json', 'r') as result:
    data = json.loads(result.read())
    for item in data:
      payload = {"buildArtifact": 'false', "completionDate": datetime.datetime.now().isoformat()[:-3] + 'Z'}
      participationsID = item.pop('id')
      participationsUrl = 'https://artemis.ase.in.tum.de/api/participations/{}'.format(participationsID)
      participation = requests.get(participationsUrl, headers=headers, cookies=cookies).json()
      item.update({'participation': participation})
      payload.update(item)
      response = requests.post(baseUrl, headers=headers, cookies=cookies, data=json.dumps(payload))
      if (response.status_code == 201) :
        print("result upload for student : {id} {name} success!".format(id=participationsID,
              name=(participation['student']['firstName'] + " " + participation['student']['lastName'])))
      else:
        print("upload failed for student {id} {name} with code {code}"
              .format(code=response.status_code, id=participationsID,
                      name=(participation['student']['firstName'] + " " + participation['student']['lastName'])))


authenticate()
manualResult()
