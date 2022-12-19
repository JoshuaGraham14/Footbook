from flask_wtf import Form
from wtforms import TextField
from wtforms.validators import DataRequired

class SessionForm(Form):
    value = TextField('value', validators=[DataRequired()])
