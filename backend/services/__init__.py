from flask import Blueprint

services_blueprint = Blueprint('services', __name__)

from . import scheduled_tasks