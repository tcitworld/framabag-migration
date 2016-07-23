#!/usr/bin/env python
## -*- coding: utf-8 -*-

import os, sqlite3, json, random

class Entry:
    def __init__(self, id, title, url, is_read, is_fav, content):
        self.id = id
        self.title = title
        self.url = url
        self.is_read = is_read
        self.is_fav = is_fav
        self.content = content
        self.tags = []

    def addTag(self, tag):
        self.tags.append(tag)

def serialiseur_perso(obj):
    if isinstance(obj, Entry):
        return {"__class__": "Entry",
                "id": obj.id,
                "title": obj.title,
                "url": obj.url,
                "is_read": obj.is_read,
                "is_fav": obj.is_fav,
                "content": obj.content,
                "tags": obj.tags}
    raise TypeError(repr(obj) + " n'est pas sérialisable !")

def exportEntries(id, collection):
    with open("export-" + str(id) + ".json", "w") as fichier:
        json.dump(collection, fichier, default=serialiseur_perso)


def fetchEntries(id, path):
    conn = sqlite3.connect(path + '/db/poche.sqlite')

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
    exportEntries(id, entries_collection)
    conn.close()

def importEntries(id):
    os.chdir("wallabag/")
    os.system("bin/console wallabag:import " + str(id) + " ../export-" + str(id) + ".json")

def createAccount(path):
    conn = sqlite3.connect(path + '/db/poche.sqlite')
    c = conn.cursor()

    c.execute('SELECT username, email from users')

    user = c.fetchone()
    password = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))

    os.chdir("wallabag/")
    os.system("bin/console fos:user:create " + user[0] + " " + user[1] + " " + password)

folderList = next(os.walk('.'))[1]
print(str(len(folderList)) + " accounts to proceed")
for i in range(0, len(folderList)):
    print("Creating account...")
    createAccount(folderList[i])
    print("Starting to export entries...")
    fetchEntries(i+1, folderList[i])
    print("Starting to import entries...")
    importEntries(i+1)
    print("Account " + str(i+1) + " on " + str(len(folderList) +1) + " processed")
