from decimal import Decimal

from apps.inventory.models import (
    InventoryTransaction,
    Stock,
)

from apps.inventory.exceptions import (
    InsufficientStockError,
    InvalidQuantityError,
    InactiveProductError,
    InactiveWarehouseError,
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

    def test_transfer_product_should_fail_when_quantity_is_zero(self):

        with self.assertRaises(InvalidQuantityError):

            self.inventory_service.issue_product(
                warehouse=self.warehouse,
                product=self.product,
                quantity=Decimal("0"),
                user=self.user,
            )

    def test_transfer_product_should_fail_when_quantity_is_negative(self):

        with self.assertRaises(InvalidQuantityError):

            self.inventory_service.issue_product(
                warehouse=self.warehouse,
                product=self.product,
                quantity=Decimal("-5"),
                user=self.user,
            )

    def test_transfer_product_should_fail_when_product_is_inactive(self):

        self.product.is_active = False
        self.product.save()

        with self.assertRaises(InactiveProductError):

            self.inventory_service.transfer_product(
                source_warehouse=self.warehouse,
                destination_warehouse=self.second_warehouse,
                product=self.product,
                quantity=Decimal("10"),
                user=self.user,
            )

    def test_transfer_product_should_fail_when_source_warehouse_is_inactive(self):

        self.warehouse.is_active = False
        self.warehouse.save()

        with self.assertRaises(InactiveWarehouseError):

            self.inventory_service.transfer_product(
                source_warehouse=self.warehouse,
                destination_warehouse=self.second_warehouse,
                product=self.product,
                quantity=Decimal("10"),
                user=self.user,
            )

    def test_transfer_product_should_fail_when_destination_warehouse_is_inactive(self):

        self.second_warehouse.is_active = False
        self.second_warehouse.save()

        with self.assertRaises(InactiveWarehouseError):

            self.inventory_service.transfer_product(
                source_warehouse=self.warehouse,
                destination_warehouse=self.second_warehouse,
                product=self.product,
                quantity=Decimal("10"),
                user=self.user,
            )
