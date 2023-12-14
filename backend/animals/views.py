# backend/animals/views.py
# Importing the blueprint
from . import animals_blueprint

# Importing necessary Flask and SQLAlchemy components
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.inspection import inspect

# Importing your models and schemas
from .models import Animal  # Import the Animal model
from .schemas import AnimalSchema  # Import the AnimalSchema for serialization

# Import the database instance (db) directly
from backend.app import db


@animals_blueprint.route('/')
class Animals(MethodView):
    @animals_blueprint.response(200, AnimalSchema(many=True))
    def get(self):
        """List all animals with pagination"""
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)  # default to 10 items per page
        paginated_animals = Animal.query.paginate(page, per_page, error_out=False)
        animals = paginated_animals.items
        return animals


    @animals_blueprint.arguments(AnimalSchema)
    @animals_blueprint.response(201, AnimalSchema)
    def post(self, new_data):
        """Add a new animal"""
        animal = Animal(**new_data)
        try:
            db.session.add(animal)  # Add the new animal to the session
            db.session.commit()  # Commit the session to save the animal
        except SQLAlchemyError as e:
            db.session.rollback()  # Rollback the transaction in case of error
            return {"message": str(e)}, 400  # Return an error message and a 400 status code
        return animal


@animals_blueprint.route('/<int:animal_id>')
class AnimalById(MethodView):
    @animals_blueprint.response(200, AnimalSchema)
    def get(self, animal_id):
        """Get animal by ID"""
        animal = Animal.query.get(animal_id)  # Retrieve an animal by ID
        return animal

    @animals_blueprint.arguments(AnimalSchema)
    @animals_blueprint.response(200, AnimalSchema)
    def put(self, update_data, animal_id):
        """Update an existing animal"""
        animal = Animal.query.get(animal_id)  # Retrieve an animal by ID
        if not animal:
            return {"message": "Animal not found"}, 404
        # Get a list of field names for the Animal model
        field_names = [column.name for column in inspect(Animal).attrs]
        try:
            for key, value in update_data.items():
                if key in field_names and key not in ['id', 'created_at']: # Exclude fields that shouldn't be updated
                    setattr(animal, key, value)
            db.session.commit()  # Commit the session to save the changes
        except SQLAlchemyError as e:
            db.session.rollback()  # Rollback the transaction in case of error
            return {"message": str(e)}, 400  # Return an error message and a 400 status code
        return animal


    @animals_blueprint.response(204)
    def delete(self, animal_id):
        """Delete an animal"""
        animal = Animal.query.get(animal_id)  # Retrieve an animal by ID
        if not animal:
            return {"message": "Animal not found"}, 404
        try:
            db.session.delete(animal)  # Delete the animal from the session
            db.session.commit()  # Commit the session to delete the animal
        except SQLAlchemyError as e:
            db.session.rollback()  # Rollback the transaction in case of error
            return {"message": str(e)}, 400  # Return an error message and a 400 status code
        return '', 204  # Return an empty response with a 204 status code
