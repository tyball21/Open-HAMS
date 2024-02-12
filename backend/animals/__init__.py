from flask import Blueprint

animals_blueprint = Blueprint('animals', 'animals', url_prefix='/animals', description='Operations on animals')

# Import routes after the Blueprint instance is created
from . import views
