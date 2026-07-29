from apps.products.models import Category


def seed():

    categories = [
        {
            "name": "Electronics",
            "description": "Electronic devices and accessories",
        },
        {
            "name": "Computer Parts",
            "description": "Computer hardware components",
        },
        {
            "name": "Networking",
            "description": "Network equipment",
        },
        {
            "name": "Storage",
            "description": "Storage devices",
        },
    ]

    for category in categories:
        Category.objects.get_or_create(
            name=category["name"],
            defaults=category,
        )