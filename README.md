### PGdP Grades Upload script (Beta)

------

#### dependency

- python 3

#### Usage

- Change the username and password in config.json
- copy the tum id list to the tumIDs in config.json
- change the course id and exercise id to the course and exercise you want to grade (30 for PGdP and 40 for PGdP Testkurs)
- run GetResult.py so a score.csv will be created with the participationsID for each student.
- write your grades and feedbacks in result.json
- Run UploadGrades.py to upload to Artemis.