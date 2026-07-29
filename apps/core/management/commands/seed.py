from django.core.management.base import BaseCommand

from .seeders import (
    role_seeder,
    country_seeder,
    province_seeder,
    city_seeder,
    unit_seeder,
    brand_seeder,
    category_seeder,
)


class Command(BaseCommand):

    help = "Seed initial data"

    def handle(self, *args, **kwargs):

        role_seeder.seed()
        country_seeder.seed()
        province_seeder.seed()
        city_seeder.seed()
        unit_seeder.seed()
        brand_seeder.seed()
        category_seeder.seed()
        
        self.stdout.write(
            self.style.SUCCESS("Seed completed successfully.")
        )