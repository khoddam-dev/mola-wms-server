from decimal import Decimal

from apps.inventory.models import (
    InventoryTransaction,
    Stock,
)
from apps.inventory.exceptions import (
    InsufficientStockError,
)

from .base import InventoryBaseTest


class IssueProductTestCase(InventoryBaseTest):

    def setUp(self):
        super().setUp()

        self.inventory_service.receive_product(
            warehouse=self.warehouse,
            product=self.product,
            quantity=Decimal("100"),
            user=self.user,
        )

    def test_issue_product_should_decrease_stock(self):

        quantity = Decimal("30")

        self.inventory_service.issue_product(
            warehouse=self.warehouse,
            product=self.product,
            quantity=quantity,
            user=self.user,
        )

        stock = Stock.objects.get(
            warehouse=self.warehouse,
            product=self.product,
        )

        self.assertEqual(
            stock.quantity,
            Decimal("70"),
        )

        transaction = InventoryTransaction.objects.filter(
            stock=stock,
            transaction_type=InventoryTransaction.TransactionType.OUT,
        ).first()

        self.assertEqual(
            transaction.transaction_type,
            InventoryTransaction.TransactionType.OUT,
        )

        self.assertEqual(
            transaction.quantity,
            quantity,
        )

    def test_issue_product_should_fail_when_stock_is_not_available(self):

        quantity = Decimal("200")

        with self.assertRaises(InsufficientStockError):

            self.inventory_service.issue_product(
                warehouse=self.warehouse,
                product=self.product,
                quantity=quantity,
                user=self.user,
            )