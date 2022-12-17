from flask import render_template, flash, redirect, session, url_for, request, g

from app import app, db, admin
from flask_admin.contrib.sqla import ModelView

from .models import Student, Module, Staff

from .forms import StudentForm, StaffForm, ModuleForm

admin.add_view(ModelView(Student, db.session))

@app.route("/")
def homepage():
        return render_template('index.html',
                               title='homepage',
                             )
@app.route('/create_student', methods=['GET','POST'])
def create_student():
    form = StudentForm()
    flash('Errors="%s"' %
          (form.errors))
    if form.validate_on_submit():
        t = Student(firstname=form.firstname.data, surname = form.surname.data, year=form.year.data)
        for modId  in form.modules.data:
            mod = Module.query.get(modId)
            t.modules.append(mod)
        db.session.add(t)
        db.session.commit()
        return redirect('/students')

    return render_template('create_student.html',
                           title='Create Student',
                           form=form)

@app.route('/create_staff', methods=['GET','POST'])
def create_staff():
    form = StaffForm()
    flash('Errors="%s"' %
          (form.errors))
    if form.validate_on_submit():
        t = Staff(firstname=form.firstname.data, surname = form.surname.data, title=form.title.data)
        db.session.add(t)
        db.session.commit()
        return redirect('/staff')

    return render_template('create_staff.html',
                           title='Create Staff',
                           form=form)

@app.route('/create_module', methods=['GET','POST'])
def create_module():
    form = ModuleForm()
    flash('Errors="%s"' %
          (form.errors))
    if form.validate_on_submit():
        t = Module(title=form.title.data)
        for studid in form.students.data:
            student = Student.query.get(studid)
            t.students.append(student)
        staff = Staff.query.get(form.staff.data)
        print(staff)
        t.staff = staff
        db.session.add(t)
        db.session.commit()
        return redirect('/modules')

    return render_template('create_module.html',
                           title='Create Module',
                           form=form)

@app.route('/students', methods=['GET'])
def getAllStudents():
    students = Student.query.all()
    return render_template('student_list.html',
                           title='All Student',
                           students=students)

@app.route('/module/<id>/students', methods=['GET'])
def getAllStudentOnModule(id):
    module = Module.query.filter_by(moduleCode=id).first()
    return render_template('student_list.html',
                           title='Students on ' + module.title,
                           students=module.students)

@app.route('/modules', methods=['GET'])
def getAllModules():
    modules = Module.query.all()
    return render_template('module_list.html',
                           title='All Modules',
                           modules=modules)

@app.route('/modules/<id>', methods=['GET'])
def getAllModulesTaughtBy(id):
    staff = Staff.query.filter_by(id=id).first()
    return render_template('module_list.html',
                           title='Modules taught by ' + str(staff),
                           modules=staff.modules)

@app.route('/modules/students/<id>', methods=['GET'])
def getAllModulesTakenBy(id):
    s = Student.query.filter_by(studentId=id).first()
    return render_template('module_list.html',
                           title='Modules taken by ' + str(s),
                           modules=s.modules)

@app.route('/staff', methods=['GET'])
def getAllStaff():
    staff = Staff.query.all()
    return render_template('staff_list.html',
                           title='All Staff',
                           staff=staff)


@app.route('/edit_student/<id>', methods=['GET','POST'])
def edit_student(id):
    student = Student.query.get(id)
    form = StudentForm(obj=student)
    flash('Errors="%s"' %
          (form.errors))
    if form.validate_on_submit():
        t = student
        t.firstname = form.firstname.data
        t.surname = form.surname.data
        t.year = form.year.data
        for modId  in form.modules.data:
            mod = Module.query.get(modId)
            t.modules.append(mod)
        db.session.commit()
        return redirect('/students')

    return render_template('edit_student.html',
                           title='Edit Student',
                           form=form)

@app.route('/edit_staff/<id>', methods=['GET','POST'])
def edit_staff(id):
    staff = Staff.query.get(id)
    form = StaffForm(obj=staff)
    flash('Errors="%s"' %
          (form.errors))
    if form.validate_on_submit():
        t = staff
        t.firstname = form.firstname.data
        t.surname = form.surname.data
        t.title = form.title.data
        db.session.commit()
        return redirect('/staff')

    return render_template('edit_staff.html',
                           title='Edit Staff',
                           form=form)

@app.route('/delete_student/<id>', methods=['GET'])
def delete_student(id):
    student = Student.query.get(id)
    db.session.delete(student)
    db.session.commit()
    return redirect('/students')

@app.route('/delete_staff/<id>', methods=['GET'])
def delete_staff(id):
    staff = Staff.query.get(id)
    db.session.delete(staff)
    db.session.commit()
    return redirect('/staff')

@app.route('/delete_module/<id>', methods=['GET'])
def delete_module(id):
    module = Module.query.get(id)
    db.session.delete(module)
    db.session.commit()
    return redirect('/modules')
