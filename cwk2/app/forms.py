from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import TextAreaField
from wtforms import DateField
from wtforms.validators import DataRequired

#Create Assessment Form:
#includes two string fields, Date field and TextArea field:
class CreatePostForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    description = TextAreaField('description', validators=[DataRequired()])