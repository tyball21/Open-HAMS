# backend/users/views.py
# Importing the blueprint
from . import users_blueprint

# Importing necessary Flask and SQLAlchemy components
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError
from flask import request

# Importing your models and schemas
from .models import User  # Import the User model
from .schemas import UserSchema  # Import the UserSchema for serialization

# Import the database instance (db) directly
from backend.app import db


@users_blueprint.route('/')
class Users(MethodView):
    @users_blueprint.response(200, UserSchema(many=True))
    def get(self):
        """List all users with pagination"""
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)  # default to 10 items per page
        paginated_users = User.query.paginate(page, per_page, error_out=False)
        users = paginated_users.items
        return users

    @users_blueprint.arguments(UserSchema)
    @users_blueprint.response(201, UserSchema)
    def post(self, new_data):
        """Add a new user"""
        user = User(**new_data)
        try:
            db.session.add(user)  # Add the new user to the session
            db.session.commit()  # Commit the session to save the user
        except SQLAlchemyError as e:
            db.session.rollback()  # Rollback the transaction in case of error
            return {"message": str(e)}, 400  # Return an error message and a 400 status code
        return user


@users_blueprint.route('/<int:user_id>')
class UserById(MethodView):
    @users_blueprint.response(200, UserSchema)
    def get(self, user_id):
        """Get user by ID"""
        user = User.query.get(user_id)  # Retrieve a user by ID
        return user

    @users_blueprint.arguments(UserSchema)
    @users_blueprint.response(200, UserSchema)
    def put(self, update_data, user_id):
        """Update an existing user"""
        user = User.query.get(user_id)  # Retrieve a user by ID
        if not user:
            return {"message": "User not found"}, 404
        # Example of updating user data, adjust as per your User model
        try:
            for key, value in update_data.items():
                if hasattr(user, key) and key not in ['id', 'created_at']:  # Exclude fields that shouldn't be updated
                    setattr(user, key, value)
            db.session.commit()  # Commit the session to save the changes
        except SQLAlchemyError as e:
            db.session.rollback()  # Rollback the transaction in case of error
            return {"message": str(e)}, 400  # Return an error message and a 400 status code
        return user

    @users_blueprint.response(204)
    def delete(self, user_id):
        """Delete a user"""
        user = User.query.get(user_id)  # Retrieve a user by ID
        if not user:
            return {"message": "User not found"}, 404
        try:
            db.session.delete(user)  # Delete the user from the session
            db.session.commit()  # Commit the session to delete the user
        except SQLAlchemyError as e:
            db.session.rollback()  # Rollback the transaction in case of error
            return {"message": str(e)}, 400  # Return an error message and a 400 status code
        return '', 204  # Return an empty response with a 204 status code
