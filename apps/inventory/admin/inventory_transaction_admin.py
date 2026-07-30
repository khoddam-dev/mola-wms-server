from django.contrib import admin

from apps.inventory.models import InventoryTransaction

def has_change_permission(self, request, obj=None):
    return False


def has_delete_permission(self, request, obj=None):
    return False

@admin.register(InventoryTransaction)
class InventoryTransactionAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "warehouse",
        "product",
        "transaction_type",
        "quantity",
        "user",
        "created_at",
    )

    search_fields = (
        "stock__product__name",
        "stock__product__code",
        "reference",
        "description",
        "user__username",
    )

    list_filter = (
        "transaction_type",
        "stock__warehouse",
        "created_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "-created_at",
    )