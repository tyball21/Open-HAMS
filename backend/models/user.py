from datetime import datetime
from .. import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    _password_hash = db.Column(db.String)
    role = db.Column(db.String)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    zoo_id = db.Column(db.Integer, db.ForeignKey('zoo.id'))
    # Relationships
    memberships = db.relationship('Membership', backref='user')
    role = db.relationship('Role', backref='users')
    animal_events_in = db.relationship('AnimalEvent', foreign_keys='AnimalEvent.user_in_id')
    animal_events_out = db.relationship('AnimalEvent', foreign_keys='AnimalEvent.user_out_id')
    animal_comments = db.relationship('AnimalComment', backref='user')
    user_events = db.relationship('UserEvent', backref='user')
    animal_audits = db.relationship('AnimalAudit', backref='user')

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')

    @password.setter
    def password(self, password):
        self._password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self._password_hash, password)