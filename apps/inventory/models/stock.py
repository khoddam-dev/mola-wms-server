from decimal import Decimal

from django.db import models

from apps.core.models import BaseModel
from apps.products.models import Product
from apps.warehouse.models import Warehouse

from apps.inventory.exceptions import InsufficientStockError


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

    def is_available(self, quantity: Decimal) -> bool:
        return self.quantity >= quantity

    def increase(self, quantity: Decimal):
        self.quantity += quantity

    def decrease(self, quantity):

        if not self.is_available(quantity):
            raise InsufficientStockError()

        self.quantity -= quantity
