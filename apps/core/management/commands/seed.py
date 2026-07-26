from django.core.management.base import BaseCommand

from apps.identity.models import Role


class Command(BaseCommand):

    help = "Seed initial system data"

    def handle(self, *args, **options):
        roles = [
            "Administrator",
            "Warehouse Manager",
            "Viewer",
        ]

        for role_name in roles:
            Role.objects.get_or_create(name=role_name)

        self.stdout.write(self.style.SUCCESS("Initial data seeded successfully."))
