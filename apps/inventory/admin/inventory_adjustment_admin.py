from django.contrib import admin

from apps.inventory.models import InventoryAdjustment


@admin.register(InventoryAdjustment)
class InventoryAdjustmentAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "stock",
        "user",
        "quantity_before",
        "quantity_after",
        "difference",
        "reason",
        "created_at",
    )

    list_filter = (
        "reason",
        "created_at",
    )

    search_fields = (
        "stock__product__name",
        "stock__warehouse__name",
        "user__username",
    )

    readonly_fields = (
        "difference",
        "created_at",
        "updated_at",
    )

    ordering = ("-created_at",)
