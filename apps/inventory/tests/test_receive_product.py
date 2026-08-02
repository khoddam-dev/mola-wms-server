from decimal import Decimal

from apps.inventory.models import (
    InventoryTransaction,
    Stock,
)

from .base import InventoryBaseTest

class ReceiveProductTestCase(InventoryBaseTest):

    def test_receive_product_should_increase_stock(self):

        # Arrange
        quantity = Decimal("100")

        # Act
        self.inventory_service.receive_product(
            warehouse=self.warehouse,
            product=self.product,
            quantity=quantity,
            user=self.user,
        )

        # Assert
        stock = Stock.objects.get(
            warehouse=self.warehouse,
            product=self.product,
        )

        self.assertEqual(
            stock.quantity,
            quantity,
        )

        transaction = InventoryTransaction.objects.get(stock=stock)

        self.assertEqual(
            transaction.transaction_type,
            InventoryTransaction.TransactionType.IN,
        )

        self.assertEqual(
            transaction.quantity,
            quantity,
        )