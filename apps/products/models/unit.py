from django.db import models

from apps.core.models import BaseModel


class Unit(BaseModel):

    name = models.CharField(
        max_length=100,   
    )

    symbol = models.CharField(
        max_length=20,
        unique=True,
    )

    class Meta:
        db_table = "units"
        verbose_name = "Unit"
        verbose_name_plural = "Units"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.symbol})"