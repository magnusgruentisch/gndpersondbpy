import sqlite3
import os
from archive_entry import archive_entry
from flask import Flask, render_template, request, g
app = Flask(__name__)
app.config.from_object(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'db/archive_entry.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)



@app.route('/')
def hello_world():
    return render_template('index.html', title="Archiver's Workbench")


@app.route('/saveArchiveEntry', methods=['POST'])
def saveArchiveEntry():
    gnd = request.form['gnd']
    nachname = request.form['nachname']
    vorname = request.form['vorname']
    url = request.form['url']
    page = request.form['page']
    comment = request.form['comment']
    ok = request.form['ok']
    entry = archive_entry(gnd, vorname, nachname, url, page, comment, ok)
    save_archive_entry(entry)

    return "heyhey " +gnd



## DB

def save_archive_entry(archive_entry):
    db = get_db()

    db.execute("insert into archiveentry values (?,?,?,?,?,?,?)",
               [archive_entry.gnd,
                archive_entry.vorname,
                archive_entry.nachname,
                archive_entry.url,
                archive_entry.page,
                archive_entry.comment,
                archive_entry.ok])
    db.commit()

@app.route('/showAll')
def show_entries():
    db = get_db()
    cur = db.execute('select * from entries order by id desc')
    entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries)




def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


if __name__ == '__main__':
    app.run(debug=True)

