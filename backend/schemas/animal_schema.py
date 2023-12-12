from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from models.animal import Animal

class AnimalSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Animal
        load_instance = True
        sqla_session = db.session

    id = auto_field()
    name = auto_field()
    kind = auto_field()
    species = auto_field()
    image = auto_field()
    max_daily_checkouts = auto_field()
    max_checkout_hours = auto_field()
    rest_time = auto_field()
    description = auto_field()
    checked_in = auto_field()
    handling_enabled = auto_field()
    created_at = auto_field()
    updated_at = auto_field()
    zoo_id = auto_field()

    # Optional: Nested relationships, uncomment if needed
    # animal_events = ma.Nested('AnimalEventSchema', many=True, exclude=('animal',))
    # animal_comments = ma.Nested('AnimalCommentSchema', many=True, exclude=('animal',))
    # audits = ma.Nested('AnimalAuditSchema', many=True, exclude=('animal',))
    # health_logs = ma.Nested('AnimalHealthLogSchema', many=True, exclude=('animal',))
    # activity_logs = ma.Nested('AnimalActivityLogSchema', many=True, exclude=('animal',))
