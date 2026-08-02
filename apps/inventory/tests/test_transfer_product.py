from decimal import Decimal

from apps.inventory.models import (
    InventoryTransaction,
    Stock,
)
from apps.inventory.exceptions import (
    InsufficientStockError,
    SameWarehouseTransferError,
)

from .base import InventoryBaseTest


class TransferProductTestCase(InventoryBaseTest):

    def setUp(self):
        super().setUp()

        self.inventory_service.receive_product(
            warehouse=self.warehouse,
            product=self.product,
            quantity=Decimal("100"),
            user=self.user,
        )

    def test_transfer_product_should_move_stock_between_warehouses(self):

        quantity = Decimal("30")

        self.inventory_service.transfer_product(
            source_warehouse=self.warehouse,
            destination_warehouse=self.second_warehouse,
            product=self.product,
            quantity=quantity,
            user=self.user,
        )

        source_stock = Stock.objects.get(
            warehouse=self.warehouse,
            product=self.product,
        )

        destination_stock = Stock.objects.get(
            warehouse=self.second_warehouse,
            product=self.product,
        )

        self.assertEqual(
            source_stock.quantity,
            Decimal("70"),
        )

        self.assertEqual(
            destination_stock.quantity,
            Decimal("30"),
        )


        self.assertTrue(
            InventoryTransaction.objects.filter(
                stock=source_stock,
                transaction_type=InventoryTransaction.TransactionType.OUT,
                quantity=quantity,
            ).exists()
        )


        self.assertTrue(
            InventoryTransaction.objects.filter(
                stock=destination_stock,
                transaction_type=InventoryTransaction.TransactionType.IN,
                quantity=quantity,
            ).exists()
        )


    def test_transfer_product_should_fail_when_stock_is_not_available(self):

        quantity = Decimal("200")

        with self.assertRaises(InsufficientStockError):

            self.inventory_service.transfer_product(
                source_warehouse=self.warehouse,
                destination_warehouse=self.second_warehouse,
                product=self.product,
                quantity=quantity,
                user=self.user,
            )


    def test_transfer_product_should_fail_when_warehouses_are_same(self):

        with self.assertRaises(SameWarehouseTransferError):

            self.inventory_service.transfer_product(
                source_warehouse=self.warehouse,
                destination_warehouse=self.warehouse,
                product=self.product,
                quantity=Decimal("10"),
                user=self.user,
            )