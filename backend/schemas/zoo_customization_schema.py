from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from models.zoo_customization import ZooCustomization

class ZooCustomizationSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ZooCustomization
        load_instance = True  # Optional: deserialize to model instances
        sqla_session = db.session  # Provide SQLAlchemy session

    id = auto_field()
    zoo_id = auto_field()
    theme_mode = auto_field()
    logo_url = auto_field()
