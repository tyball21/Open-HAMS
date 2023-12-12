from datetime import datetime
from . import db.JSON

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)  # e.g., 'admin', 'moderator'
    permissions = db.Column(db.JSON)  # Store a JSON object with specific permissions

	