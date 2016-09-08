#!/usr/bin/env python3
## -*- coding: utf-8 -*-

import os, sqlite3, json, random, string, time, sys
from Entry import Entry, serialiseur_perso


def exportEntries(name, collection):
    filename = "json/" + str(name) + ".json"
    with open(filename, "w") as fichier:
        json.dump(collection, fichier, default=serialiseur_perso)
    print("Exported file " + filename)

def fileExists(name):
    print("File json/" + str(name) + ".json exists")
    return os.path.isfile("json/" + str(name) + ".json")

def fetchEntries(path):
    conn = sqlite3.connect('../u/' + path + '/db/poche.sqlite')

    c = conn.cursor()

    c.execute('SELECT e.id, e.title, e.url, e.is_read, e.is_fav, e.content, t.value from entries e left join tags_entries te on e.id = te.entry_id left join tags t on te.tag_id = t.id')

    entries = c.fetchall()

    entry_previous = None
    entries_collection = []
    for entry in entries:
        if (entry_previous != None and entry[0] != entry_previous.id):
            entryObj = Entry(entry[0], entry[1], entry[2], entry[3], entry[4], entry[5])
            entry_previous = entryObj
            if (entry[6] != None):
                entryObj.addTag(entry[6])
            entries_collection.append(entryObj)
        elif entry_previous != None and entry[0] == entry_previous.id and entry[6] != None:
            entry_previous.addTag(entry[6])
        else:
            entryObj = Entry(entry[0], entry[1], entry[2], entry[3], entry[4], entry[5])
            entry_previous = entryObj
            if (entry[6] != None):
                entryObj.addTag(entry[6])
            entries_collection.append(entryObj)
    exportEntries(path, entries_collection)
    conn.close()

#def importEntries(id):
#    filename = "json/export-" + str(id) + ".json"
#    print("Trying to import file " + filename)
#    os.system("wallabag/bin/console wallabag:import " + str(id) + " " + filename + " --env=prod")

folderList = next(os.walk('../u/'))[1]
errors = []
print(str(len(folderList)) + " accounts to proceed")
k = 0
for i in range(0, len(folderList)):
    print("Exporting entries...")
    try:
        fetchEntries(folderList[i])
    except sqlite3.OperationalError:
        print("Error while retrieving entries. Adding " + folderList[i] + "to the list of errored accounts")
        errors.append(folderList[i])
    print("Account " + str(i+1) + " on " + str(len(folderList) +1) + " processed")

with open('errors-export.json', 'w') as fp:
    json.dump(errors, fp)
