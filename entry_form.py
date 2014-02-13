from flask.ext.wtf import Form
from wtforms import TextField, BooleanField
from wtforms.validators import Required

class ArchiveEntryForm(Form):
    gnd = TextField('gnd', validators = [Required()])
    vorname = TextField('vorname')
    nachname = TextField('nachname')
    url = TextField('url')
    page = TextField('page')
    comment = TextField('comment')
    ok = BooleanField('ok', default = False)