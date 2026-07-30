from django.contrib import admin

from apps.inventory.models import Stock


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "warehouse",
        "product",
        "quantity",
        "is_active",
    )

    search_fields = (
        "product__name",
        "product__code",
        "warehouse__name",
    )

    list_filter = (
        "warehouse",
        "is_active",
    )

    ordering = (
        "warehouse",
        "product",
    )