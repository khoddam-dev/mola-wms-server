from django.contrib import admin

from apps.core.models import Province


@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "country", "is_active")
    search_fields = ("name",)
    list_filter = ("country", "is_active")