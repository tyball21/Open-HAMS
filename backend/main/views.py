# backend/main/views.py

from . import main_blueprint

@main_blueprint.route('/')
def home():
    return "Welcome to OpenHAMSv8"
