# backend/animals/views.py
from . import animals_blueprint
from flask.views import MethodView
from .models import Animal  # assuming you have an Animal model in models.py
from .schemas import AnimalSchema  # assuming you have an AnimalSchema in schemas.py


@animals_blueprint.route('/')
class Animals(MethodView):
    @animals_blueprint.response(200, AnimalSchema(many=True))
    def get(self):
        """List all animals"""
        animals = Animal.query.all()  # or however you get all animals
        return animals

    @animals_blueprint.arguments(AnimalSchema)
    @animals_blueprint.response(201, AnimalSchema)
    def post(self, new_data):
        """Add a new animal"""
        animal = Animal(**new_data)
        # add code to save the new animal to the database
        return animal

@animals_blueprint.route('/<int:animal_id>')
class AnimalById(MethodView):
    @animals_blueprint.response(200, AnimalSchema)
    def get(self, animal_id):
        """Get animal by ID"""
        animal = Animal.query.get(animal_id)  # or however you get an animal by ID
        return animal

    @animals_blueprint.arguments(AnimalSchema)
    @animals_blueprint.response(200, AnimalSchema)
    def put(self, update_data, animal_id):
        """Update an existing animal"""
        animal = Animal.query.get(animal_id)  # or however you get an animal by ID
        # add code to update the animal in the database
        return animal

    @animals_blueprint.response(204)
    def delete(self, animal_id):
        """Delete an animal"""
        # add code to delete the animal from the database