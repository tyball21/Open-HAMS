from datetime import datetime
from .permissions import roles_permissions
from .. import db


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)  # e.g., 'admin', 'moderator'
    # Link roles to permissions
    permissions = db.relationship('Permission', secondary=roles_permissions, backref=db.backref('roles', lazy='dynamic'))
