from django.contrib import admin

from apps.core.models import Country


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "code", "is_active")
    search_fields = ("name", "code")
    list_filter = ("is_active",)