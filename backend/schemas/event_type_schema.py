from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from models.event_type import EventType

class EventTypeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = EventType
        load_instance = True
        sqla_session = db.session

    id = auto_field()
    name = auto_field()
    created_at = auto_field()
    updated_at = auto_field()
    zoo_id = auto_field()

    # Optional: Nested relationships, uncomment if needed
    # events = ma.Nested('EventSchema', many=True, exclude=('event_type',))
