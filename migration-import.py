#!/usr/bin/env python3
## -*- coding: utf-8 -*-

print("Getting list of users")

import mysql.connector, random, string, os, json

def importEntries(id, user):
    filename = "json/" + user + ".json"
    print("Trying to import file " + filename)
    os.system("wallabag/bin/console wallabag:import " + str(id) + " " + filename + " --env=prod")

conn = mysql.connector.connect(host="localhost",user="root",password="po1Ay5guawi7Paqu", database="c1_wallabag")
cursor = conn.cursor()
cursor.execute("SELECT id, username FROM wallabag_user")
rows = cursor.fetchall()
nbRows = len(rows)
errors = []
for row in rows:
    if os.path.isfile("json/" + row[1] + ".json"):
        importEntries(row[0], row[1])
    else:
        print("no json file exists for this user.")
        errors.append(row[1])

with open('errors-import.json', 'w') as fp:
        json.dump(errors, fp)


