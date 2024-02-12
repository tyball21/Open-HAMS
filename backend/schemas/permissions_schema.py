from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from models.permissions import Permission
from backend import db


class PermissionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Permission
        load_instance = True
        sqla_session = db.session

    id = auto_field()
    name = auto_field()
