from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///animals.db'
db = SQLAlchemy(app)


class Animal(db.Model):
    __tablename__ = 'animal'
    id = db.Column(db.Integer, primary_key=True)
    animal_type = db.Column(db.String(50))
    name = db.Column(db.String(100))
    birth_date = db.Column(db.Date)
    breed = db.Column(db.String(100))  # Добавляем столбец "breed"
    photo = db.Column(db.String(255))  # Поле для фотографии, если она у вас есть

    # Остальной код вашей модели
