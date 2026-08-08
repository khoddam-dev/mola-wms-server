from decimal import Decimal

from apps.inventory.models import InventoryAdjustment, InventoryTransaction
from apps.inventory.services.inventory_service import InventoryService

from .base import InventoryBaseTest


class AdjustProductTestCase(InventoryBaseTest):

    def setUp(self):

        super().setUp()

        self.stock.quantity = Decimal("100")
        self.stock.save(
            update_fields=[
                "quantity",
                "updated_at",
            ]
        )

    def test_adjust_product_should_increase_stock(self):
        adjustment = self.inventory_service.adjust_product(
            stock=self.stock,
            actual_quantity=Decimal("110"),
            user=self.user,
            reason="Cycle count",
        )

        self.stock.refresh_from_db()

        self.assertEqual(
            self.stock.quantity,
            Decimal("110"),
        )

        self.assertEqual(
            adjustment.quantity_before,
            Decimal("100"),
        )

        self.assertEqual(
            adjustment.quantity_after,
            Decimal("110"),
        )

        self.assertEqual(
            adjustment.difference,
            Decimal("10"),
        )

        transaction = InventoryTransaction.objects.get(
            stock=self.stock,
        )

        self.assertEqual(
            transaction.transaction_type,
            InventoryTransaction.TransactionType.ADJUSTMENT_IN,
        )

        self.assertEqual(
            transaction.quantity,
            Decimal("10"),
        )

    def test_adjust_product_should_decrease_stock(self):
        adjustment = self.inventory_service.adjust_product(
            stock=self.stock,
            actual_quantity=Decimal("90"),
            user=self.user,
            reason="Cycle count",
        )

        self.stock.refresh_from_db()

        self.assertEqual(
            self.stock.quantity,
            Decimal("90"),
        )

        self.assertEqual(
            adjustment.quantity_before,
            Decimal("100"),
        )

        self.assertEqual(
            adjustment.quantity_after,
            Decimal("90"),
        )

        self.assertEqual(
            adjustment.difference,
            Decimal("-10"),
        )

        transaction = InventoryTransaction.objects.get(
            stock=self.stock,
        )

        self.assertEqual(
            transaction.transaction_type,
            InventoryTransaction.TransactionType.ADJUSTMENT_OUT,
        )

        self.assertEqual(
            transaction.quantity,
            Decimal("10"),
        )

    def test_adjust_product_should_create_adjustment_without_transaction_when_quantity_is_equal(
        self,
    ):
        adjustment = self.inventory_service.adjust_product(
            stock=self.stock,
            actual_quantity=Decimal("100"),
            user=self.user,
            reason="Cycle count",
        )

        self.stock.refresh_from_db()

        self.assertEqual(
            self.stock.quantity,
            Decimal("100"),
        )

        self.assertEqual(
            adjustment.quantity_before,
            Decimal("100"),
        )

        self.assertEqual(
            adjustment.quantity_after,
            Decimal("100"),
        )

        self.assertEqual(
            adjustment.difference,
            Decimal("0"),
        )

        self.assertFalse(
            InventoryTransaction.objects.filter(
                stock=self.stock,
            ).exists()
        )

        self.assertEqual(
            InventoryAdjustment.objects.filter(
                stock=self.stock,
            ).count(),
            1,
        )
