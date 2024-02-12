from datetime import datetime
from . import db

class AnimalEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    animal_id = db.Column(db.Integer, db.ForeignKey('animal.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    user_in_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    user_out_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    checked_in = db.Column(db.DateTime, nullable=True)
    checked_out = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    duration = db.Column(db.Interval, nullable=True)
    zoo_id = db.Column(db.Integer, db.ForeignKey('zoo.id'))
    event_type_id = db.Column(db.Integer, db.ForeignKey('event_type.id'))
    event_type = db.relationship('EventType', backref='animal_events')