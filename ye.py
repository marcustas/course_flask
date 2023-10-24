from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///animals.db'
db = SQLAlchemy(app)

class Animal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    breed = db.Column(db.String(100), nullable=False)
    photo = db.Column(db.String(200), nullable=False)
    date_of_birth = db.Column(db.DateTime, nullable=False)

    @property
    def age(self):
        import datetime
        today = datetime.date.today()
        age = today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return age

@app.route('/add_animal', methods=['POST'])
def add_animal():
    breed = request.form.get('breed')
    photo = request.form.get('photo')
    date_of_birth = request.form.get('date_of_birth')

    new_animal = Animal(breed=breed, photo=photo, date)