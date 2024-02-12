from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from models.animal_comment import AnimalComment
from backend import db

class AnimalCommentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = AnimalComment
        load_instance = True
        sqla_session = db.session

    id = auto_field()
    animal_id = auto_field()
    user_id = auto_field()
    event_id = auto_field()
    text = auto_field()
    created_at = auto_field()
    updated_at = auto_field()
    zoo_id = auto_field()

    # Optional: Nested relationships, uncomment if needed
    # animal = ma.Nested('AnimalSchema', only=['id', 'name', 'species'])
    # user = ma.Nested('UserSchema', only=['id', 'email', 'first_name', 'last_name'])
    # event = ma.Nested('EventSchema', only=['id', 'name', 'start_at', 'end_at'])
