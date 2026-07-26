from django.db import models

from apps.core.models import BaseModel


class Role(BaseModel):

    name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = "roles"
        verbose_name = "Role"
        verbose_name_plural = "Roles"

    def __str__(self):
        return self.name
