from app import db
from models import Role

def seed_roles():
    roles = [
        {"name": "Admin", "permissions": {"manage_animals": True, "edit_zoo_settings": True, ...}},
        {"name": "Moderator", "permissions": {"manage_animals": True, "edit_zoo_settings": False, ...}},
        {"name": "Standard User", "permissions": {"manage_animals": False, "edit_zoo_settings": False, ...}}
    ]

    for role_data in roles:
        role = Role(name=role_data["name"], permissions=role_data["permissions"])
        db.session.add(role)

    db.session.commit()

if __name__ == "__main__":
    seed_roles()
