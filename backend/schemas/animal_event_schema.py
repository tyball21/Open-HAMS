from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from models.animal_event import AnimalEvent

class AnimalEventSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = AnimalEvent
        load_instance = True
        sqla_session = db.session

    id = auto_field()
    animal_id = auto_field()
    event_id = auto_field()
    user_in_id = auto_field()
    user_out_id = auto_field()
    checked_out = auto_field()
    checked_in = auto_field()
    created_at = auto_field()
    updated_at = auto_field()
    zoo_id = auto_field()

    # Optional: Nested relationships, uncomment if needed
    animal = ma.Nested('AnimalSchema', only=['id', 'name', 'species'])
    event = ma.Nested('EventSchema', only=['id', 'name', 'start_at', 'end_at'])
    user_in = ma.Nested('UserSchema', only=['id', 'email', 'first_name', 'last_name'])
    user_out = ma.Nested('UserSchema', only=['id', 'email', 'first_name', 'last_name'])
