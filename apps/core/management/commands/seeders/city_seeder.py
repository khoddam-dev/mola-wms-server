from apps.core.models import Province, City


def seed():

    fars = Province.objects.get(name="Fars")

    cities = [
        {
            "name": "Shiraz",
            "province": fars,
            "is_active": True,
        },
    ]

    for city in cities:
        City.objects.get_or_create(
            name=city["name"],
            province=city["province"],
            defaults={
                "is_active": city["is_active"],
            },
        )