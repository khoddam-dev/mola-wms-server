from apps.products.models import Unit


def seed():

    units = [
        {"name": "Piece", "symbol": "pcs"},
        {"name": "Kilogram", "symbol": "kg"},
        {"name": "Gram", "symbol": "g"},
        {"name": "Liter", "symbol": "l"},
        {"name": "Meter", "symbol": "m"},
        {"name": "Box", "symbol": "box"},
        {"name": "Pack", "symbol": "pack"},
    ]

    for unit in units:
        Unit.objects.get_or_create(
            symbol=unit["symbol"],
            defaults=unit,
        )