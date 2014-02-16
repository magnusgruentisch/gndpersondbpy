# README

Diese kleine Anwendung beruht auf Flask. http://flask.pocoo.org/.


## Installation

1. Lesen: http://flask.pocoo.org/docs/installation/.
2. Befolgen.
3. Starten.


## Setup

1. Die sqlite3 muss unter db liegen und heisst archive_entry.db
2. git clone git://github.com/lepture/flask-wtf.git
3. sudo pip install rdflib
4. Install DB
4.1. mkdir db
4.2. cd db 
4.3. sqlite3 archive_entry.db < ../schema.sql
5. Install DB Plan B 
5.1. mkdir db
5.2. sqlite3 db/archive_entry.db
5.3. Einfuegen von Inhalt von schema.sql
6. pip install requests
