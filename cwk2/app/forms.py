from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import PasswordField
from wtforms import TextAreaField
from wtforms import BooleanField
from wtforms import SelectField
from wtforms.validators import DataRequired, Regexp, Email, EqualTo

teams=["Arsenal", "Aston Villa", "Bournemouth", "Brentford", "Brighton & Hove Albion", "Chelsea", "Crystal Palace",
"Everton", "Fulham", "Leeds United", "Leicester City", "Liverpool", "Manchester City", "Manchester United",
"Newcastle United", "Nottingham Forest", "Southampton", "Tottenham Hotspur", "West Ham United", "Wolverhampton Wanderers"]

#Create Assessment Form:
#includes two string fields, Date field and TextArea field:
class CreatePostForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    description = TextAreaField('description', validators=[DataRequired()])

class LoginForm(FlaskForm):
    # email = StringField('email', validators=[DataRequired(), Regexp("\w+@{1}\w+", message="Must be a valid email format")])
    email = StringField('email', validators=[DataRequired(), Email(message="Must be a valid email")])
    password = PasswordField('password', validators=[DataRequired()])
    remember = BooleanField('remember')

class SignupForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email(message="Must be a valid email")])
    username = StringField('password', validators=[DataRequired()])
    team = SelectField('team', choices=list(enumerate(teams)))
    password = PasswordField('password', validators=[DataRequired()])
    passwordConfirm = PasswordField('passwordConfirm', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])