from django.db import models

from apps.core.models import BaseModel
from .brand import Brand
from .category import Category
from .unit import Unit


class Product(BaseModel):

    code = models.CharField(
        max_length=20,
        unique=True,
    )

    barcode = models.CharField(
        max_length=100,
        unique=True,
        blank=True,
        null=True,
    )

    name = models.CharField(
        max_length=255,
    )

    description = models.TextField(
        blank=True,
    )

    brand = models.ForeignKey(
        Brand,
        on_delete=models.PROTECT,
        related_name="products",
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
    )

    unit = models.ForeignKey(
        Unit,
        on_delete=models.PROTECT,
        related_name="products",
    )

    minimum_stock = models.DecimalField(
        max_digits=12,
        decimal_places=3,
        default=0,
    )

    class Meta:
        db_table = "products"
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ["name"]

    def __str__(self):
        return self.name