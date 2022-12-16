from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import TextAreaField
from wtforms import DateField
from wtforms.validators import DataRequired

#Create Assessment Form:
#includes two string fields, Date field and TextArea field:
class CreateAssessmentForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    module_code = StringField('module_code', validators=[DataRequired()])
    deadline = DateField('deadline', validators=[DataRequired()])
    description = TextAreaField('description', validators=[DataRequired()])