from django.db import models

from apps.core.models import BaseModel


class Brand(BaseModel):

    name = models.CharField(
        max_length=100,
        unique=True,
    )

    class Meta:
        db_table = "brands"
        verbose_name = "Brand"
        verbose_name_plural = "Brands"
        ordering = ["name"]

    def __str__(self):
        return self.name