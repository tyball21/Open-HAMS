from models import Permission


def has_permission(permissions: list[Permission], permission_name: str) -> bool:
    return any(permission.name == permission_name for permission in permissions)
