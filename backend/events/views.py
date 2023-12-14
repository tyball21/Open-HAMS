# backend/events/views.py
# Importing the blueprint
from . import events_blueprint

# Importing necessary Flask and SQLAlchemy components
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.inspection import inspect
from flask import request

# Importing your models and schemas
from .models import Event  # Import the Event model
from .schemas import EventSchema  # Import the EventSchema for serialization

# Import the database instance (db) directly
from backend.app import db


@events_blueprint.route('/')
class Events(MethodView):
    @events_blueprint.response(200, EventSchema(many=True))
    def get(self):
        """List all events with pagination"""
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)  # default to 10 items per page
        paginated_events = Event.query.paginate(page, per_page, error_out=False)
        events = paginated_events.items
        return events

    @events_blueprint.arguments(EventSchema)
    @events_blueprint.response(201, EventSchema)
    def post(self, new_data):
        """Add a new event"""
        event = Event(**new_data)
        try:
            db.session.add(event)  # Add the new event to the session
            db.session.commit()  # Commit the session to save the event
        except SQLAlchemyError as e:
            db.session.rollback()  # Rollback the transaction in case of error
            return {"message": str(e)}, 400  # Return an error message and a 400 status code
        return event


@events_blueprint.route('/<int:event_id>')
class EventById(MethodView):
    @events_blueprint.response(200, EventSchema)
    def get(self, event_id):
        """Get event by ID"""
        event = Event.query.get(event_id)  # Retrieve an event by ID
        return event

    @events_blueprint.arguments(EventSchema)
    @events_blueprint.response(200, EventSchema)
    def put(self, update_data, event_id):
        """Update an existing event"""
        event = Event.query.get(event_id)  # Retrieve an event by ID
        if not event:
            return {"message": "Event not found"}, 404
        # Get a list of field names for the Event model
        field_names = [column.name for column in inspect(Event).attrs]
        try:
            for key, value in update_data.items():
                if key in field_names and key not in ['id', 'created_at']: # Exclude fields that shouldn't be updated
                    setattr(event, key, value)
            db.session.commit()  # Commit the session to save the changes
        except SQLAlchemyError as e:
            db.session.rollback()  # Rollback the transaction in case of error
            return {"message": str(e)}, 400  # Return an error message and a 400 status code
        return event

    @events_blueprint.response(204)
    def delete(self, event_id):
        """Delete an event"""
        event = Event.query.get(event_id)  # Retrieve an event by ID
        if not event:
            return {"message": "Event not found"}, 404
        try:
            db.session.delete(event)  # Delete the event from the session
            db.session.commit()  # Commit the session to delete the event
        except SQLAlchemyError as e:
            db.session.rollback()  # Rollback the transaction in case of error
            return {"message": str(e)}, 400  # Return an error message and a 400 status code
        return '', 204  # Return an empty response with a 204 status code
