from decimal import Decimal

from django.core.exceptions import ValidationError
from django.conf import settings
from django.db import models

from apps.core.models import BaseModel
from .stock import Stock


class InventoryTransaction(BaseModel):

    @property
    def product(self):
        return self.stock.product

    @property
    def warehouse(self):
        return self.stock.warehouse

    class TransactionType(models.TextChoices):
        IN = "IN", "In"
        OUT = "OUT", "Out"
        ADJUSTMENT_IN = "ADJ_IN", "Adjustment In"
        ADJUSTMENT_OUT = "ADJ_OUT", "Adjustment Out"

    stock = models.ForeignKey(
        Stock,
        on_delete=models.PROTECT,
        related_name="transactions",
    )

    transaction_type = models.CharField(
        max_length=10,
        choices=TransactionType.choices,
    )

    quantity = models.DecimalField(
        max_digits=15,
        decimal_places=3,
    )

    reference = models.CharField(
        max_length=100,
        blank=True,
    )

    description = models.TextField(
        blank=True,
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="inventory_transactions",
    )

    class Meta:
        db_table = "inventory_transactions"
        verbose_name = "Inventory Transaction"
        verbose_name_plural = "Inventory Transactions"
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"{self.transaction_type} | "
            f"{self.stock.product.name} | "
            f"{self.quantity}"
        )
