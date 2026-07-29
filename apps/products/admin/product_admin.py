from django.contrib import admin

from apps.products.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "code",
        "name",
        "brand",
        "category",
        "unit",
        "minimum_stock",
        "is_active",
    )

    search_fields = (
        "code",
        "barcode",
        "name",
    )

    list_filter = (
        "brand",
        "category",
        "unit",
        "is_active",
    )

    ordering = (
        "name",
    )