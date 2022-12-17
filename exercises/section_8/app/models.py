from app import db

enrollment = db.Table('enrollment', db.Model.metadata,
    db.Column('studentId', db.Integer, db.ForeignKey('student.studentId')),
    db.Column('moduleCode', db.Integer, db.ForeignKey('module.moduleCode'))
)

class Student (db.Model):
    studentId = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(250), index=True)
    surname = db.Column(db.String(250),index=True)
    year = db.Column(db.Date)
    modules = db.relationship('Module',secondary=enrollment)
    def __repr__(self):
        return  self.firstname + ' ' + self.surname

class Module (db.Model):
    moduleCode = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(250), index=True)
    students = db.relationship('Student',secondary=enrollment, overlaps="modules")
    moduleLeader = db.Column(db.Integer, db.ForeignKey('staff.id'))
    
    def __repr__(self):
        return  self.title

class Staff (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(250), index=True)
    surname = db.Column(db.String(250), index=True)
    title = db.Column(db.String(10), index=True)
    modules = db.relationship('Module', backref='staff', lazy='dynamic')

    def __repr__(self):
        return self.title + " " + self.firstname + " " + self.surname
