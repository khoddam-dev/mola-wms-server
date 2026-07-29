from django.apps import AppConfig


class WarehouseConfig(AppConfig):
    name = "apps.warehouse"

    def ready(self):
        import apps.warehouse.admin