from flask import Flask, jsonify, request, Response, render_template

from models.pydantic.models import AnimalCreate, AnimalResponse
from typing import Union, Tuple, Dict, Any
from settings import settings
from database import init_db
from models.sqlalchemy.models import Animal

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = settings.sqlalchemy_database_uri

db = init_db(app)


@app.route('/')
def home() -> str:
    return render_template('home.html')


@app.route('/health', methods=['GET'])
def health_check() -> tuple[str, int]:
    return 'OK', 200


@app.route('/animals', methods=['GET'])
def index() -> Response:
    name = request.args.get('name')
    if name:
        animals = Animal.query.filter_by(name=name).all()
    else:
        animals = Animal.query.all()
    response = {'animals': []}
    for animal in animals:
        model = AnimalResponse.model_validate(animal)
        age = model.calculate_age()
        data = model.model_dump(mode='json')
        data['age'] = age
        response['animals'].append(data)
    json_response = jsonify(response)
    return json_response


@app.route('/animal', methods=['POST'])
def add_animal() -> tuple[Response, int]:
    data = AnimalCreate(**request.get_json())
    new_animal = Animal(
        animal_type=data.animal_type,
        animal_breed=data.animal_breed,
        name=data.name,
        photo_url=data.photo_url,
        birth_date=data.birth_date
    )
    db.session.add(new_animal)
    db.session.commit()
    return jsonify(
        {
            "message": "Animal added successfully!",
            "animal": AnimalResponse.model_validate(new_animal).model_dump(mode='json')
        }
    ), 201


@app.route('/animal/<int:pk>', methods=['PUT'])
def update_animal(pk: int) -> Union[Response, tuple[Response, int]]:
    data = AnimalCreate(**request.get_json())
    animal = Animal.query.get(pk)
    if not animal:
        return jsonify({"message": "Animal not found"}), 404

    animal.animal_type = data.animal_type
    animal.name = data.name
    animal.birth_date = data.birth_date
    animal.animal_breed = data.animal_breed
    animal.photo_url = data.photo_url
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


def initialize_app():
    with app.app_context():
        db.create_all()


if __name__ == '__main__':
    initialize_app()
    app.run(debug=True)
