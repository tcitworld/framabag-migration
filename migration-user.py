#!/usr/bin/env python3
## -*- coding: utf-8 -*-

print("Getting list of")
# folderList = next(os.walk('../u/'))[1]

import mysql.connector, random, string, os

conn = mysql.connector.connect(host="localhost",user="root",password="po1Ay5guawi7Paqu", database="c1_bag")
cursor = conn.cursor()
cursor.execute("SELECT login, email FROM accounts WHERE active = 1")
rows = cursor.fetchall()
nbRows = len(rows)
for id, row in enumerate(rows):
    print("processing row " + str(id) + " on " + str(nbRows) + " ...")
    if row[0] == None or row[0] == '' or row[0] == ' ':
        username = 'user-' + str(id)
    else:
        username = row[0]
    if row[1] == None or row[1] == '' or row[1] == ' ':
        email = 'NoEmail-' + str(id)
    else:
        email = row[1]
    while username[0] == '-':
        username = username[1:]
    password = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    print('user : ' + username)
    print('mail : ' + email)
    os.system("wallabag/bin/console fos:user:create '" + username + "' '" + email + "' '" + password + "' --env=prod")
conn.close()
print("Finished")

