from datetime import datetime
from . import db

class Zoo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))  # Name of the zoo
    location = db.Column(db.String(255))  # Location of the zoo
    information = db.Column(db.String(1024), nullable=True)  # Additional information about the zoo
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Creation timestamp
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Update timestamp
    # Relationships
    animals = db.relationship('Animal', backref='zoo')
    animal_comments = db.relationship('AnimalComment', backref='zoo')
    users = db.relationship('User', backref='zoo')
    events = db.relationship('Event', backref='zoo')
    event_types = db.relationship('EventType', backref='zoo')
    groups = db.relationship('Group', backref='zoo')
    animal_events = db.relationship('AnimalEvent', backref='zoo')
    user_events = db.relationship('UserEvent', backref='zoo')
    zoo_customization = db.relationship('ZooCustomization', backref='zoo', uselist=False)
