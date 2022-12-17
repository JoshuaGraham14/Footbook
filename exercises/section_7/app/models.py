from app import db

class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(500), index=True, unique=True)
    start_date = db.Column(db.DateTime)
    duration = db.Column(db.Integer)
    rent = db.Column(db.Float)
    landlord_id = db.Column(db.Integer, db.ForeignKey('landlord.id'))

    def __repr__(self):
            return '{}{}{}{}{}'.format(self.id, self.address, self.start_date, self.duration, self.rent)

class Landlord(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(500), index=True)
    contact_number = db.Column(db.String(20))
    address = db.Column(db.String(500), index=True, unique=True)
    properties = db.relationship('Property', backref='landlord', lazy='dynamic')

    def __repr__(self):
            return '{}{}{}'.format(self.id, self.name, self.contact_number)
