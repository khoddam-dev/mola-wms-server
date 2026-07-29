from django.contrib import admin

from apps.products.models import Unit


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "symbol",
        "is_active",
    )

    search_fields = (
        "name",
        "symbol",
    )

    list_filter = (
        "is_active",
    )

    ordering = (
        "name",
    )