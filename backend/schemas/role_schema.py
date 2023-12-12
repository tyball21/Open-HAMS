from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from models.role import Role

class RoleSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Role
        load_instance = True
        sqla_session = db.session

    id = auto_field()
    name = auto_field()
    permissions = auto_field()  # Handles the JSON field
