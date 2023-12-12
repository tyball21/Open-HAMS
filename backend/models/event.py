from datetime import datetime
from . import db

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_type_id = db.Column(db.Integer, db.ForeignKey('event_type.id'))
    name = db.Column(db.String)
    description = db.Column(db.String, nullable=True)
    start_at = db.Column(db.DateTime)
    end_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    zoo_id = db.Column(db.Integer, db.ForeignKey('zoo.id'))
    # Relationships
    animal_events = db.relationship('AnimalEvent', backref='event')
    animal_comments = db.relationship('AnimalComment', backref='event')
    user_events = db.relationship('UserEvent', backref='event')