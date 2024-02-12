from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from models.user_event import UserEvent
from backend import db

class UserEventSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = UserEvent
        load_instance = True
        sqla_session = db.session

    user_id = auto_field()
    event_id = auto_field()
    created_at = auto_field()
    updated_at = auto_field()
    zoo_id = auto_field()

    # Optional: Nested relationships, uncomment if needed
    user = ma.Nested('UserSchema', only=['id', 'email', 'first_name', 'last_name'])
    event = ma.Nested('EventSchema', only=['id', 'name', 'date', 'description'])
    zoo = ma.Nested('ZooSchema', only=['id', 'name', 'location'])
