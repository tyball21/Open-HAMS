from datetime import datetime
from backend import db

class Animal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    kind = db.Column(db.String)
    species = db.Column(db.String)
    image = db.Column(db.String, nullable=True)
    max_daily_checkouts = db.Column(db.Integer) 
    max_checkout_hours = db.Column(db.Float)    
    rest_time = db.Column(db.Float)
    # New fields for rest period management
    daily_checkout_count = db.Column(db.Integer, default=0)
    daily_checkout_duration = db.Column(db.Interval, default=timedelta(hours=0))
    last_checkin_time = db.Column(db.DateTime, nullable=True)             
    description = db.Column(db.String, nullable=True)
    checked_in = db.Column(db.Boolean, default=True)
    handling_enabled = db.Column(db.Boolean)    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    zoo_id = db.Column(db.Integer, db.ForeignKey('zoo.id'))
    # Relationships
    animal_events = db.relationship('AnimalEvent', backref='animal') # 
    animal_comments = db.relationship('AnimalComment', backref='animal')
    audits = db.relationship('AnimalAudit', backref='animal')
    health_logs = db.relationship('AnimalHealthLog', backref='animal')
    activity_logs = db.relationship('AnimalActivityLog', backref='animal')
