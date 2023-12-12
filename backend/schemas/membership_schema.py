from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from models.membership import Membership

class MembershipSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Membership
        load_instance = True
        sqla_session = db.session

    user_id = auto_field()
    group_id = auto_field()
    created_at = auto_field()
    updated_at = auto_field()

    # Optional: Nested relationships, uncomment if needed
    # user = ma.Nested('UserSchema', only=['id', 'email', 'first_name', 'last_name'])
    # group = ma.Nested('GroupSchema', only=['id', 'name'])
