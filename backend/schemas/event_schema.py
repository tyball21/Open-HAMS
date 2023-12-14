

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from models.event import Event

class EventSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Event
        load_instance = True
        sqla_session = db.session

    id = auto_field()
    event_type_id = auto_field()
    name = auto_field()
    description = auto_field()
    start_at = auto_field()
    end_at = auto_field()
    created_at = auto_field()(dump_only=True)
    updated_at = auto_field()(dump_only=True)
    zoo_id = auto_field()

    # Optional: Nested relationships, uncomment if needed
    # animal_events = ma.Nested('AnimalEventSchema', many=True, exclude=('event',))
    # animal_comments = ma.Nested('AnimalCommentSchema', many=True, exclude=('event',))
    # user_events = ma.Nested('UserEventSchema', many=True, exclude=('event',))
