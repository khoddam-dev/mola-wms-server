from django.db import models
from apps.core.models import BaseModel
from apps.identity.models import User

from .stock import Stock


class InventoryAdjustment(BaseModel):
    """
    Represents a stock count adjustment record.
    """

    stock = models.ForeignKey(
        Stock,
        on_delete=models.PROTECT,
        related_name="adjustments",
    )

    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="inventory_adjustments",
    )

    quantity_before = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    quantity_after = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    reason = models.CharField(
        max_length=255,
    )

    description = models.TextField(
        blank=True,
    )

    class Meta:
        db_table = "inventory_adjustments"
        ordering = ["-created_at"]
        verbose_name = "Inventory Adjustment"
        verbose_name_plural = "Inventory Adjustments"

    @property
    def difference(self):
        return self.quantity_after - self.quantity_before

    def __str__(self):
        return f"{self.stock.product.name} - " f"{self.difference}"
