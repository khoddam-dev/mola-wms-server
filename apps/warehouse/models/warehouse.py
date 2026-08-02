from django.db import models
from django.conf import settings

from apps.core.models import BaseModel, City
from django.core.validators import MinValueValidator


class Warehouse(BaseModel):

    name = models.CharField(max_length=150)

    code = models.CharField(
        max_length=settings.WAREHOUSE_CODE_LENGTH,
        unique=True,
    )

    city = models.ForeignKey(
        City,
        on_delete=models.PROTECT,
        related_name="warehouses",
    )

    address = models.TextField(blank=True)

    capacity = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
    )

    description = models.TextField(
        blank=True,
    )

    class Meta:
        db_table = "warehouses"
        ordering = ["name"]
        verbose_name = "Warehouse"
        verbose_name_plural = "Warehouses"

    def __str__(self):
        return f"{self.code} - {self.name}"