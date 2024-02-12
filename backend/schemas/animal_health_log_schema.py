from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from models.animal_health_log import AnimalHealthLog
from backend import db

class AnimalHealthLogSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = AnimalHealthLog
        load_instance = True
        sqla_session = db.session

    id = auto_field()
    animal_id = auto_field()
    health_details = auto_field()
    logged_at = auto_field()

    # Optional: Nested relationships, uncomment if needed
    # animal = ma.Nested('AnimalSchema', only=['id', 'name', 'species'])
