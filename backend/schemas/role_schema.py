from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from models.role import Role
from models.permissions import Permission  # Import the Permission model
from backend import db

class RoleSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Role
        load_instance = True
        sqla_session = db.session

    id = auto_field()
    name = auto_field()
    # Serialize permissions as nested objects
    permissions = ma.Nested('PermissionSchema', many=True)
