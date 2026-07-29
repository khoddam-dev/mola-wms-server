from apps.core.models import Country, Province


def seed():

    iran = Country.objects.get(code="IRN")

    provinces = [
        {
            "name": "Fars",
            "country": iran,
            "is_active": True,
        },
    ]

    for province in provinces:
        Province.objects.get_or_create(
            name=province["name"],
            country=province["country"],
            defaults={
                "is_active": province["is_active"],
            },
        )