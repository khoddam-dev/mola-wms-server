from django.db import models

from apps.core.models import BaseModel
from apps.products.models import Product
from apps.warehouse.models import Warehouse


class Stock(BaseModel):

    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.PROTECT,
        related_name="stocks",
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="stocks",
    )

    quantity = models.DecimalField(
        max_digits=15,
        decimal_places=3,
        default=0,
    )

    class Meta:
        db_table = "stocks"
        verbose_name = "Stock"
        verbose_name_plural = "Stocks"
        ordering = ["warehouse", "product"]

        constraints = [
            models.UniqueConstraint(
                fields=["warehouse", "product"],
                name="unique_product_per_warehouse",
            )
        ]

    def __str__(self):
        return f"{self.warehouse} - {self.product}"