from app import db

#Assessment Database Model
class Assessment(db.Model):
    id = db.Column(db.Integer, primary_key=True) #primary key 
    title = db.Column(db.String(200)) #string max char length 200
    module_code = db.Column(db.String(100)) #string max char length 100
    deadline = db.Column(db.DateTime) #DateTime data type
    description = db.Column(db.String(1000)) #string max char length 1000
    status = db.Column(db.Boolean) #Boolean data type