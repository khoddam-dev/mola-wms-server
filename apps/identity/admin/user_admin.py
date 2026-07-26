from django.contrib import admin

from apps.identity.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "first_name",
        "last_name",
        "role",
        "is_active",
    )

    search_fields = (
        "username",
        "first_name",
        "last_name",
        "mobile",
    )

    list_filter = (
        "role",
        "is_active",
    )
