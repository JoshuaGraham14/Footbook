from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, DateField, TextAreaField, SelectMultipleField, SelectField
from wtforms.validators import DataRequired
from .models import Student, Module, Staff

class StudentForm(FlaskForm):
    firstname = StringField('firstname', validators=[DataRequired()])
    surname = StringField('surname', validators=[DataRequired()])
    year = DateField('year', validators=[DataRequired()])
    choices = [(g.moduleCode, g.title) for g in Module.query.order_by('title')]
    modules =  SelectMultipleField('modules', coerce=int ,choices = choices)

class ModuleForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    ss = [(s.studentId, s.firstname+ " "+ s.surname) for s in Student.query.order_by('surname')]
    students =  SelectMultipleField('students', coerce=int ,choices = ss)
    staffs = [(s.id, s.firstname+ " "+ s.surname) for s in Staff.query.order_by('surname')]
    staff = SelectField('staff', coerce=int,choices=staffs)

class StaffForm(FlaskForm):
    firstname = StringField('firstname', validators=[DataRequired()])
    surname = StringField('surname', validators=[DataRequired()])
    title = SelectField('firstname', choices = [('Mr','Mr'),('Ms','Ms'),('Mrs','Mrs'),('Miss','Miss'),('Dr','Dr'),('Prof','Prof'),],validators=[DataRequired()])
