from datetime import datetime
from . import db

class ZooCustomization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    zoo_id = db.Column(db.Integer, db.ForeignKey('zoo.id'), unique=True)
    theme_mode = db.Column(db.String)
    logo_url = db.Column(db.String, nullable=True)