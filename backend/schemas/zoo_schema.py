from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from models.zoo import Zoo

class ZooSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Zoo
        load_instance = True  # Optional: deserialize to model instances
        sqla_session = db.session  # Provide SQLAlchemy session

    id = auto_field()
    name = auto_field()
    location = auto_field()
    information = auto_field()
    created_at = auto_field()
    updated_at = auto_field()

  
    animals = auto_field()
    animal_comments = auto_field()
    users = auto_field()
    events = auto_field()
    event_types = auto_field()
    groups = auto_field()
    animal_events = auto_field()
    user_events = auto_field()
    zoo_customization = auto_field()
