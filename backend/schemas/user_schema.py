from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from models.user import User
from backend import db

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        sqla_session = db.session
        exclude = ('_password_hash',)  # Exclude the password hash field

    id = auto_field()
    email = auto_field()
    first_name = auto_field()
    last_name = auto_field()
    # Do not include the password or its hash
    role = auto_field()
    role_id = auto_field()
    created_at = auto_field()
    updated_at = auto_field()
    zoo_id = auto_field()

    # Relationships - Uncomment if needed
    memberships = ma.Nested('MembershipSchema', many=True, exclude=('user',))
    role = ma.Nested('RoleSchema', exclude=('users',))
    animal_events_in = ma.Nested('AnimalEventSchema', many=True, exclude=('user_in',))
    animal_events_out = ma.Nested('AnimalEventSchema', many=True, exclude=('user_out',))
    animal_comments = ma.Nested('AnimalCommentSchema', many=True, exclude=('user',))
    user_events = ma.Nested('UserEventSchema', many=True, exclude=('user',))
    animal_audits = ma.Nested('AnimalAuditSchema', many=True, exclude=('user',))
