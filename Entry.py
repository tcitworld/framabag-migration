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
        return {"id": obj.id,
                "title": obj.title,
                "url": obj.url,
                "is_read": obj.is_read,
                "is_fav": obj.is_fav,
                "content": obj.content,
                "tags": obj.tags}
    raise TypeError(repr(obj) + " n'est pas sérialisable !")
