from flask import Flask, jsonify, request, Response, render_template
from models.pydantic.models import AnimalCreate, AnimalResponse
from typing import Union
from settings import settings
from database import init_db
from models.sqlalchemy.models import Animal
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = settings.sqlalchemy_database_uri

db = init_db(app)


@app.route('/')
def home() -> str:
    return render_template('home.html')


@app.route('/health', methods=['GET'])  # Додали ендпоінт /health
def health_check():
    return 'OK', 200


@app.route('/animals', methods=['GET'])
def index() -> Response:
    animals = Animal.query.all()
    return jsonify({"animals": [AnimalResponse.model_validate(animal).model_dump(mode='json') for animal in animals]})



@app.route('/animal', methods=['POST'])
def add_animal() -> tuple[Response, int]:
    data = AnimalCreate(**request.get_json())
    new_animal = Animal(
        animal_type=data.animal_type,
        name=data.name,
        birth_date=data.birth_date,
        breed=data.breed,
        photo=data.photo,
    )
    db.session.add(new_animal)
    db.session.commit()

    animal_response = AnimalResponse.model_validate(new_animal)
    if animal_response:
        return jsonify(
            {
                "message": "Animal added successfully!",
                "animal": animal_response.model_dump(mode='json')
            }
        ), 201
    else:
        return jsonify({"message": "Failed to validate animal data"}), 400



@app.route('/animal/<int:pk>', methods=['PUT'])
def update_animal(pk: int) -> Union[Response, tuple[Response, int]]:
    data = AnimalCreate(**request.get_json())
    animal = Animal.query.get(pk)
    if not animal:
        return jsonify({"message": "Animal not found"}), 404

    animal.animal_type = data.animal_type
    animal.name = data.name
    animal.birth_date = data.birth_date
    animal.breed = data.breed
    animal.photo = data.photo
    db.session.commit()
    return jsonify(
        {
            "message": "Animal updated successfully!",
            "animal": AnimalResponse.model_validate(animal).model_dump(mode='json'),
        },
    )


@app.route('/animal/<int:pk>', methods=['GET'])
def retrieve_animal(pk: int) -> Union[Response, tuple[Response, int]]:
    animal = Animal.query.get(pk)
    if not animal:
        return jsonify({"message": "Animal not found"}), 404

    return jsonify(
        {
            "animal": AnimalResponse.model_validate(animal).model_dump(mode='json'),
        }
    )


@app.route('/animal/<int:pk>', methods=['DELETE'])
def delete_animal(pk: int) -> Union[Response, tuple[Response, int]]:
    animal = Animal.query.get(pk)
    if not animal:
        return jsonify({"message": "Animal not found"}), 404

    db.session.delete(animal)
    db.session.commit()
    return jsonify({"message": "Animal deleted successfully!"})


@app.route('/search', methods=['GET'])  # Додали ендпоінт для пошуку за іменем
def search_animal():
    name = request.args.get('name', '')
    animals = Animal.query.filter(Animal.name.like(f'%{name}%')).all()
    return jsonify({"animals": [AnimalResponse.model_validate(animal).model_dump(mode='json') for animal in animals]})


def calculate_age(birth_date):
    today = datetime.now()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age


def initialize_app():
    with app.app_context():
        db.create_all()


if __name__ == '__main__':
    initialize_app()
    app.run(debug=True)
