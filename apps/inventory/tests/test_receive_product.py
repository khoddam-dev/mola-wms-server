from decimal import Decimal

from .base import InventoryBaseTest

from apps.inventory.models import (
    InventoryTransaction,
    Stock,
)

from apps.inventory.exceptions import (
    InvalidQuantityError,
    InactiveProductError,
    InactiveWarehouseError,
)


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

    def test_receive_product_should_fail_when_quantity_is_zero(self):

        with self.assertRaises(InvalidQuantityError):

            self.inventory_service.receive_product(
                warehouse=self.warehouse,
                product=self.product,
                quantity=Decimal("0"),
                user=self.user,
            )

    def test_receive_product_should_fail_when_quantity_is_negative(self):

        with self.assertRaises(InvalidQuantityError):

            self.inventory_service.receive_product(
                warehouse=self.warehouse,
                product=self.product,
                quantity=Decimal("-5"),
                user=self.user,
            )

    def test_receive_product_should_fail_when_product_is_inactive(self):

        self.product.is_active = False
        self.product.save()

        with self.assertRaises(InactiveProductError):

            self.inventory_service.receive_product(
                warehouse=self.warehouse,
                product=self.product,
                quantity=Decimal("10"),
                user=self.user,
            )

    def test_receive_product_should_fail_when_warehouse_is_inactive(self):

        self.warehouse.is_active = False
        self.warehouse.save()

        with self.assertRaises(InactiveWarehouseError):

            self.inventory_service.receive_product(
                warehouse=self.warehouse,
                product=self.product,
                quantity=Decimal("10"),
                user=self.user,
            )