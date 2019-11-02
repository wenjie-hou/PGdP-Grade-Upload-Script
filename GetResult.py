# coding=utf-8

import csv
import json
import requests

config = json.loads(open("config.json", "r").read())

exercisesID = config['exerciseID']
courseid = config['courseID']
username = config['username']
password = config['password']
idString = config['tumIDs']
listOfIDs = idString.split(", ")

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


def writecsv():
  url0 = "https://artemis.ase.in.tum.de/api/courses/{course}/exercises/{exercise}/results?showAllResults=all" \
         "&ratedOnly=true&withSubmissions=false&withAssessors=false".format(course=courseid, exercise=exercisesID)
  res = requests.get(url0, headers=headers, cookies=cookies)
  print(res.status_code)
  data = res.json()
  resFile = open('response.json', 'w', encoding='utf-8')
  output = [x for x in data if x['participation']['student']['login'] in listOfIDs]
  json.dump(output, resFile, ensure_ascii=False)
  resFile.close()
  with open("score.csv", "w") as file:
    writer = csv.writer(file)
    header = ['result', 'score', 'tum-id', 'firstName', 'lastName', 'email', 'repositoryUrl', 'buildPlanUrl',
              'participation-Id']
    row1 = []
    row2 = []
    row3 = []
    row4 = []
    row5 = []
    row6 = []
    row7 = []
    row8 = []
    row9 = []
    for key in output:
      row1.append(key['resultString'])
      row2.append(str(key['score']))
      row3.append(key['participation']['student']['login'])
      row4.append(key['participation']['student']['firstName'])
      row5.append(key['participation']['student']['lastName'])
      row6.append(key['participation']['student']['email'])
      row7.append(key['participation']['repositoryUrl'])
      row8.append(
        'https://bamboobruegge.in.tum.de/chain/viewChain.action?planKey=' + key['participation']['buildPlanId'])
      row9.append(key['participation']['id'])
    writer.writerow(header)
    for i in zip(row1, row2, row3, row4, row5, row6, row7, row8, row9):
      file.write("{},{},{},{},{},{},{},{},{}\n".format(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8]))
    print("complete!")


authenticate()
writecsv()
