from django.db import models

from apps.core.models import BaseModel
from .province import Province


class City(BaseModel):

    name = models.CharField(max_length=100)

    province = models.ForeignKey(
        Province,
        on_delete=models.PROTECT,
        related_name="cities",
    )

    class Meta:
        db_table = "cities"
        ordering = ["name"]
        verbose_name = "City"
        verbose_name_plural = "Cities"
        constraints = [
            models.UniqueConstraint(
                fields=["province", "name"],
                name="unique_city_per_province",
            )
        ]

    def __str__(self):
        return self.name