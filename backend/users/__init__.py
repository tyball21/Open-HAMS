from flask import Blueprint

users_blueprint = Blueprint('users', 'users', url_prefix='/users', description='Operations on users')

# Import routes after the Blueprint instance is created
from . import views
