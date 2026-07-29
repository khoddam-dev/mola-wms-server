from apps.identity.models import Role


def seed():
    roles = [
        {"name": "Administrator"},
        {"name": "Warehouse Manager"},
        {"name": "Viewer"},
    ]

    for role in roles:
        Role.objects.get_or_create(
            name=role["name"],
            defaults=role,
        )