from django.db import models

from apps.core.models import BaseModel
from .country import Country


class Province(BaseModel):

    name = models.CharField(max_length=100)

    country = models.ForeignKey(
        Country,
        on_delete=models.PROTECT,
        related_name="provinces",
    )

    class Meta:
        db_table = "provinces"
        ordering = ["name"]
        verbose_name = "Province"
        verbose_name_plural = "Provinces"
        constraints = [
            models.UniqueConstraint(
                fields=["country", "name"],
                name="unique_province_per_country",
            )
        ]

    def __str__(self):
        return self.name