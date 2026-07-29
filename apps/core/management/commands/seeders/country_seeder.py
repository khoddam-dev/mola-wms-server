from apps.core.models import Country


def seed():
    countries = [
        {
            "name": "Iran",
            "code": "IRN",
            "is_active": True,
        },
    ]

    for country in countries:
        Country.objects.get_or_create(
            code=country["code"],
            defaults=country,
        )