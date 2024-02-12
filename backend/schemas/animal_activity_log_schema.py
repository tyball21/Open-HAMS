from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from models.animal_activity_log import AnimalActivityLog
from backend import db

class AnimalActivityLogSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = AnimalActivityLog
        load_instance = True
        sqla_session = db.session

    id = auto_field()
    animal_id = auto_field()
    activity_details = auto_field()
    logged_at = auto_field()

    # Optional: Nested relationship, uncomment if needed
    # animal = ma.Nested('AnimalSchema', only=['id', 'name', 'species'])
