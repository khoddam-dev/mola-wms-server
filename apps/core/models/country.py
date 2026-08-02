from django.db import models

from apps.core.models import BaseModel


class Country(BaseModel):

    name = models.CharField(max_length=100, unique=True)

    code = models.CharField(max_length=3, unique=True)

    class Meta:
        db_table = "countries"
        ordering = ["name"]
        verbose_name = "Country"
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.name