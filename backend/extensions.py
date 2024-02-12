# backend/extensions.py

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_vite import Vite
from flask_smorest import Api

# Instantiate extensions without passing the Flask app object
db = SQLAlchemy()
ma = Marshmallow()
vite = Vite()
api = Api()
