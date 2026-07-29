from apps.products.models import Brand


def seed():

    brands = [
        {"name": "Samsung"},
        {"name": "LG"},
        {"name": "ASUS"},
        {"name": "Intel"},
        {"name": "AMD"},
        {"name": "Kingston"},
        {"name": "Seagate"},
        {"name": "Western Digital"},
    ]

    for brand in brands:
        Brand.objects.get_or_create(
            name=brand["name"],
            defaults=brand,
        )