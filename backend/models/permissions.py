from models import Role
from .. import db

roles_permissions = db.Table('roles_permissions',
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True),
    db.Column('permission_id', db.Integer, db.ForeignKey('permission.id'), primary_key=True)
)

class Permission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)  # e.g., 'manage_animals', 'edit_zoo_settings'

    roles = db.relationship('Role', secondary=roles_permissions, backref=db.backref('permissions', lazy='dynamic'))

