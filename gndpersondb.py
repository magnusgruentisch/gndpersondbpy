import sqlite3
import os
from flask import Flask, render_template, request, g
app = Flask(__name__)
app.config.from_object(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'archive_entry.db'),
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

    return "heyhey " +gnd



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

