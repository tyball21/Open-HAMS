# backend/factory.py

from flask import Flask
from .extensions import db, ma, vite, api  # Assuming these are initialized without the app object
from .models import (Zoo, Animal, User, ZooCustomization, Role, Event, EventType, 
                     Group, Membership, AnimalEvent, AnimalComment, UserEvent, 
                     AnimalAudit, AnimalHealthLog, AnimalActivityLog)
from .main import main_blueprint
from .animals import animals_blueprint



class Config:
    """Base config."""
    # common config like SECRET_KEY

class DevelopmentConfig(Config):
    """Development config."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@localhost/openhamshogelzoodb'  # dev database URI

class TestingConfig(Config):
    """Testing config."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = '...'  # test database URI

class ProductionConfig(Config):
    """Production config."""
    SQLALCHEMY_DATABASE_URI = '...'  # prod database URI

def create_app(config_class):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    ma.init_app(app)
    vite.init_app(app)
    api.init_app(app)

    # Import and register your blueprints here
    app.register_blueprint(main_blueprint)
    app.register_blueprint(animals_blueprint)

    return app
