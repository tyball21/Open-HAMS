# Purpose: This model appears to track changes to the animal's data itself, such as changes in its status or other attributes.


from datetime import datetime
from . import db

class AnimalAudit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    animal_id = db.Column(db.Integer, db.ForeignKey('animal.id'))
    changed_field = db.Column(db.String)
    old_value = db.Column(db.String, nullable=True)
    new_value = db.Column(db.String, nullable=True)
    changed_at = db.Column(db.DateTime, default=datetime.utcnow)
    changed_by = db.Column(db.Integer, db.ForeignKey('user.id'))