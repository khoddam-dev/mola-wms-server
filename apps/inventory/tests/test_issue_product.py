from decimal import Decimal

from .base import InventoryBaseTest

from apps.inventory.models import (
    InventoryTransaction,
    Stock,
)

from apps.inventory.exceptions import (
    InsufficientStockError,
    InvalidQuantityError,
    InactiveProductError,
    InactiveWarehouseError,
)



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

        with self.assertRaises(InsufficientStockError):

            self.inventory_service.issue_product(
                warehouse=self.warehouse,
                product=self.product,
                quantity=Decimal("200"),
                user=self.user,
            )

    def test_issue_product_should_fail_when_quantity_is_zero(self):

        with self.assertRaises(InvalidQuantityError):

            self.inventory_service.issue_product(
                warehouse=self.warehouse,
                product=self.product,
                quantity=Decimal("0"),
                user=self.user,
            )

    def test_issue_product_should_fail_when_quantity_is_negative(self):

        with self.assertRaises(InvalidQuantityError):

            self.inventory_service.issue_product(
                warehouse=self.warehouse,
                product=self.product,
                quantity=Decimal("-5"),
                user=self.user,
            )

    def test_issue_product_should_fail_when_product_is_inactive(self):

        self.product.is_active = False
        self.product.save()

        with self.assertRaises(InactiveProductError):

            self.inventory_service.issue_product(
                warehouse=self.warehouse,
                product=self.product,
                quantity=Decimal("10"),
                user=self.user,
            )

    def test_issue_product_should_fail_when_warehouse_is_inactive(self):

        self.warehouse.is_active = False
        self.warehouse.save()

        with self.assertRaises(InactiveWarehouseError):

            self.inventory_service.issue_product(
                warehouse=self.warehouse,
                product=self.product,
                quantity=Decimal("10"),
                user=self.user,
            )
