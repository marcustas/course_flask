from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from pydantic import BaseModel
from flask import request

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///animals.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Animal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    breed = db.Column(db.String(100))
    birth_date = db.Column(db.Date)
    photo_url = db.Column(db.String(200))

class AnimalFilter(BaseModel):
    name: str

@app.route('/health')
def health_check():
    return '', 200

@app.route('/animals', methods=['GET'])
def get_animals():
    animals = Animal.query.all()
    return jsonify([animal.__dict__ for animal in animals])

@app.route('/animals', methods=['POST'])
def create_animal():
    data = request.json
    animal = Animal(**data)
    db.session.add(animal)
    db.session.commit()
    return jsonify(animal.__dict__), 201

@app.route('/animals/<int:id>', methods=['GET'])
def get_animal(id):
    animal = Animal.query.get(id)
    if animal:
        return jsonify(animal.__dict__)
    else:
        return 'Animal not found', 404

@app.route('/animals/<int:id>', methods=['PUT'])
def update_animal(id):
    data = request.json
    animal = Animal.query.get(id)
    if animal:
        for key, value in data.items():
            setattr(animal, key, value)
        db.session.commit()
        return jsonify(animal.__dict__)
    else:
        return 'Animal not found', 404

@app.route('/animals/<int:id>', methods=['DELETE'])
def delete_animal(id):
    animal = Animal.query.get(id)
    if animal:
        db.session.delete(animal)
        db.session.commit()
        return '', 204
    else:
        return 'Animal not found', 404

if __name__ == '__main__':
    app.run(debug=True)

def get_filtered_animals():
    name = request.args.get('name')
    if name:
        filtered_animals = Animal.query.filter_by(name=name).all()
        return jsonify([animal.__dict__ for animal in filtered_animals])
    else:
        animals = Animal.query.all()
        return jsonify([animal.__dict__ for animal in animals])

    #aaa