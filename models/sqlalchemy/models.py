from database import db
from datetime import datetime

class Animal(db.Model):
    __tablename__ = 'animal'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    animal_type = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    birth_date = db.Column(db.Date, nullable=False)


    @property
    def age(self):
        today = datetime.now()
        age = today.year - self.birth_date.year
        return age
