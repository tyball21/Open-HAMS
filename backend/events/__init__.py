from flask import Blueprint

events_blueprint = Blueprint('events', 'events', url_prefix='/events', description='Operations on events')

# Import routes after the Blueprint instance is created
from . import views
