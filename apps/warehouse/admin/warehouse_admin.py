from django.contrib import admin

from apps.warehouse.models import Warehouse


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "code",
        "name",
        "city",
        "capacity",
        "is_active",
    )

    search_fields = (
        "code",
        "name",
    )

    list_filter = (
        "city",
        "is_active",
    )

    ordering = (
        "name",
    )