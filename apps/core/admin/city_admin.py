from django.contrib import admin

from apps.core.models import City


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "province", "is_active")
    search_fields = ("name",)
    list_filter = ("province", "is_active")