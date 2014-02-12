__author__ = 'hubert'

class archive_entry:


    def __init__(self):
        self.data = []

    def __init__(self, gnd, vorname, nachname, url, page, comment, ok):
        self.gnd = gnd
        self.vorname = vorname
        self.nachname = nachname
        self.url = url
        self.page = page
        self.comment = comment
        self.ok = ok