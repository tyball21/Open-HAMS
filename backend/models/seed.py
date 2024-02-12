from models import Role, Permission
from .. import db

def seed_permissions():
    permissions = [
        {"name": "manage_animals"},
        {"name": "manage_events"},
        {"name": "manage_users"},
        {"name": "edit_zoo_settings"},
        {"name": "create_events"},
        {"name": "checkout_animals"},
        {"name": "view_animals"},
        {"name": "view_events"},
        # ... other permissions as necessary ...
    ]

    for perm_data in permissions:
        permission = Permission(name=perm_data["name"])
        db.session.add(permission)
    db.session.commit()



def seed_roles():
    roles = [
        {"name": "Admin", "permissions": ["manage_animals", "manage_events", "manage_users", "edit_zoo_settings"]},
        {"name": "Moderator", "permissions": ["manage_animals", "manage_events"]},
        {"name": "Standard User", "permissions": ["create_events", "checkout_animals", "view_animals", "view_events"]}
    ]

    for role_data in roles:
        role = Role(name=role_data["name"])
        for perm_name in role_data["permissions"]:
            perm = Permission.query.filter_by(name=perm_name).first()
            if perm:
                role.permissions.append(perm)
        db.session.add(role)

    db.session.commit()

if __name__ == "__main__":
    seed_permissions()
    seed_roles()

