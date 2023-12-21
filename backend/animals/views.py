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

    def update_animal_status(self):
    """
    Updates the checked_in status of all animals based on current time and event schedules.
    """
    animals = Animal.query.all()
    current_time = datetime.utcnow()

    for animal in animals:
        # Assuming AnimalEvent model links animals to events
        animal_events = AnimalEvent.query.filter(
            AnimalEvent.animal_id == animal.id,
            AnimalEvent.checked_out <= current_time,
            AnimalEvent.checked_in >= current_time
        ).all()

        if animal_events:
            animal.checked_in = False  # Animal is part of an ongoing event
        else:
            animal.checked_in = True  # No ongoing event for this animal

    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error updating animal status: {e}")


        def log_audit(self, animal_id, changed_field, old_value, new_value, changed_by_user_id):
        """
        Logs an audit entry for changes to an animal's record.
        :param animal_id: ID of the animal being audited.
        :param changed_field: The field that was changed.
        :param old_value: The old value of the field before change.
        :param new_value: The new value of the field after change.
        :param changed_by_user_id: ID of the user who made the change.
        """
        audit_entry = AnimalAudit(
            animal_id=animal_id,
            changed_field=changed_field,
            old_value=old_value,
            new_value=new_value,
            changed_at=datetime.utcnow(),
            changed_by=changed_by_user_id
        )
        db.session.add(audit_entry)
        db.session.commit()

    def log_activity(self, animal_id, activity_details):
        """
        Logs an activity entry for significant events involving an animal.
        :param animal_id: ID of the animal involved in the activity.
        :param activity_details: Description of the activity.
        """
        activity_log = AnimalActivityLog(
            animal_id=animal_id,
            activity_details=activity_details,
            logged_at=datetime.utcnow()
        )
        db.session.add(activity_log)
        db.session.commit()

    def update_animal_status(self):
        """
        Updates the checked_in status of all animals based on current time and event schedules.
        """
        animals = Animal.query.all()
        current_time = datetime.utcnow()

        for animal in animals:
            # Fetch events linked to the animal
            animal_events = AnimalEvent.query.filter(
                AnimalEvent.animal_id == animal.id,
                AnimalEvent.checked_out <= current_time,
                AnimalEvent.checked_in >= current_time
            ).all()

            old_status = animal.checked_in
            animal.checked_in = not animal_events  # False if animal is part of ongoing event

            # Log the status change as an activity and an audit
            if old_status != animal.checked_in:
                self.log_activity(animal.id, f"Status changed to {'Checked In' if animal.checked_in else 'Checked Out'}")
                self.log_audit(animal.id, 'checked_in', str(old_status), str(animal.checked_in), None)  # Assuming None for user ID if automated

            try:
                db.session.commit()
            except SQLAlchemyError as e:
                db.session.rollback()
                print(f"Error updating animal status: {e}")


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
        animal = Animal.query.get(animal_id)
        if not animal:
            return {"message": "Animal not found"}, 404

        # Store old values for audit logging
        old_values = {field: getattr(animal, field) for field in update_data}

        try:
            # Update animal attributes
            for key, value in update_data.items():
                if key in inspect(Animal).attrs and key not in ['id', 'created_at']:
                    setattr(animal, key, value)

            db.session.commit()

            # Log changes
            for key, new_value in update_data.items():
                if key in old_values and old_values[key] != new_value:
                    self.log_audit(animal_id, key, old_values[key], new_value, None)  # Assuming None for user ID

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"message": str(e)}, 400

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
