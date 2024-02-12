from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from models.animal_audit import AnimalAudit
from backend import db

class AnimalAuditSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = AnimalAudit
        load_instance = True
        sqla_session = db.session

    id = auto_field()
    animal_id = auto_field()
    changed_field = auto_field()
    old_value = auto_field()
    new_value = auto_field()
    changed_at = auto_field()
    changed_by = auto_field()

    # Optional: Nested relationships, uncomment if needed
    # animal = ma.Nested('AnimalSchema', only=['id', 'name', 'species'])
    # changed_by_user = ma.Nested('UserSchema', only=['id', 'email', 'first_name', 'last_name'], attribute='changed_by')
