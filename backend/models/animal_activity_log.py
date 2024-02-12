# Purpose: This model seems to be designed to track specific activities related to an animal, 
#          like being checked in or out of an event, or any other significant activity.

from datetime import datetime
from . import db

class AnimalActivityLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    animal_id = db.Column(db.Integer, db.ForeignKey('animal.id'))
    activity_details = db.Column(db.String)
    logged_at = db.Column(db.DateTime, default=datetime.utcnow)