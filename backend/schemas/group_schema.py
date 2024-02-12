from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from models.group import Group
from backend import db

class GroupSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Group
        load_instance = True
        sqla_session = db.session

    id = auto_field()
    title = auto_field()
    created_at = auto_field()
    updated_at = auto_field()
    zoo_id = auto_field()

    # Optional: Nested relationships, uncomment if needed
    # memberships = ma.Nested('MembershipSchema', many=True, exclude=('group',))
