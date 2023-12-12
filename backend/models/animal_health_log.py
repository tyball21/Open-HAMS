from datetime import datetime
from . import db

class AnimalHealthLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    animal_id = db.Column(db.Integer, db.ForeignKey('animal.id'))
    health_details = db.Column(db.String)
    logged_at = db.Column(db.DateTime, default=datetime.utcnow)