from datetime import datetime
from . import db

class EventType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    zoo_id = db.Column(db.Integer, db.ForeignKey('zoo.id'))
    # Relationships
    events = db.relationship('Event', backref='event_type')