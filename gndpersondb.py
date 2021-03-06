import sqlite3
import os
import requests
import datetime
#from archive_entry import archive_entry
from entry_form import ArchiveEntryForm
from flask import Flask, render_template, request, g, redirect,url_for, stream_with_context, Response
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

    save_archive_entry(gnd, vorname, nachname, url, page, comment, ok)

    form = ArchiveEntryForm()
    form.gnd = gnd
    form.nachname = nachname
    form.vorname = vorname
    form.url = url
    form.page = page
    form.comment = comment
    form.ok = ok

    return render_template('confirm.html', form=form)


@app.route('/confirmArchiveEntry', methods=['POST'])
def confirmArchiveEntry():
    form = ArchiveEntryForm()
    update_archive_entry(form.gnd.data,
                         form.vorname.data,
                         form.nachname.data,
                         form.url.data,
                         form.page.data,
                         form.comment.data,
                         form.ok.data,
                         form.gnd.data)

    entries = get_all()
    return render_template('show_entries.html', entries=entries)


@app.route('/showAll')
def show_entries():
    entries = get_all()
    return render_template('show_entries.html', entries=entries)

@app.route('/showOne/<gnd>')
def show_entry(gnd):
    entry = get_one(gnd)
    print entry
    return render_template('show_entry.html', entry=entry[0])


@app.route('/exportAll')
def export_all():
    entries = get_all()
    return render_template('export.csv', entries=entries)


# staging.api.lobid.org/person?id=118580604&format=full
# payload = {'key1': 'value1', 'key2': 'value2'}
# r = requests.get("http://httpbin.org/get", params=payload)
@app.route('/gnd/<gnd>')
def gnd(gnd):
    print "[", gnd, "]"
    payload = {'id': gnd, 'format': 'full'}
    req = requests.get("http://staging.api.lobid.org/person", params=payload,  stream = True)
    return Response(stream_with_context(req.iter_content()), content_type = req.headers['content-type'])

@app.route('/getJson')
def get_json():
    return """
    {
"one": "Singular sensation",
"two": "Beady little eyes",
"three": "Little birds pitch by my doorstep"
}
"""

## DB

def save_archive_entry(gnd, vorname, nachname, url, page, comment, ok):
    """Schreibt einen Datensatz weg"""
    db = get_db()

    db.execute("insert into archiveentry values (?,?,?,?,?,?,?)",
               [gnd,
                vorname,
                nachname,
                url,
                page,
                comment,
                ok])
    db.commit()




def update_archive_entry(gnd, vorname, nachname, url, page, comment, ok, gnd_new):
    """Update eines Datensatzes"""
    db = get_db()
    print("Update:",gnd, vorname, nachname, url, page, comment, ok, gnd_new)
    db.execute("update archiveentry set gnd=?, vorname=?, nachname=?, url=?, page=?, comment=?, ok=? where gnd=?",
               [gnd,
                vorname,
                nachname,
                url,
                page,
                comment,
                ok,
                gnd_new])
    db.commit()

def get_all():
    """Holt alle Datensaetze"""
    db = get_db()
    cur = db.execute('select * from archiveentry order by gnd asc')
    entries = cur.fetchall()
    return entries


def get_one(gnd):
    """Holt einen Datensatz fuer eine gnd"""
    db = get_db()
    cur = db.execute("select * from archiveentry where gnd=?", [gnd])
    entries = cur.fetchall()
    return entries


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
    app.run(host='0.0.0.0',debug=True)

