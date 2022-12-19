from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

class SessionForm(FlaskForm):
    value = StringField('value', validators=[DataRequired()])
