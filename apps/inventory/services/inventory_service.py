from decimal import Decimal

from django.db import transaction

from apps.inventory.exceptions import (
    StockNotFoundError,
    InvalidQuantityError,
    InactiveProductError,
    InactiveWarehouseError,
    SameWarehouseTransferError,
)

from apps.products.models import Product
from apps.warehouse.models import Warehouse
from apps.inventory.models import InventoryTransaction, Stock


class InventoryService:

    def _validate_quantity(self, quantity: Decimal) -> None:
        if quantity <= 0:
            raise InvalidQuantityError("Quantity must be greater than zero.")

    def _validate_product(self, product: Product) -> None:
        if not product.is_active:
            raise InactiveProductError("Product is inactive.")

    def _validate_warehouse(self, warehouse: Warehouse) -> None:

        if not warehouse.is_active:
            raise InactiveWarehouseError("Warehouse is inactive.")

    def _validate_transfer_warehouses(
        self, source_warehouse: Warehouse, destination_warehouse: Warehouse
    ) -> None:

        if source_warehouse == destination_warehouse:
            raise SameWarehouseTransferError(
                "Source and destination warehouses must be different."
            )

    def _get_stock(self, warehouse: Warehouse, product: Product) -> Stock | None:

        try:
            return Stock.objects.filter(
                warehouse=warehouse,
                product=product,
            ).first()

        except Stock.DoesNotExist:
            raise StockNotFoundError("Stock record not found.")

    def _get_locked_stock(self, warehouse: Warehouse, product: Product) -> Stock:

        try:
            return Stock.objects.select_for_update().get(
                warehouse=warehouse,
                product=product,
            )

        except Stock.DoesNotExist:
            raise StockNotFoundError("Stock not found.")

    def _create_stock(self, warehouse: Warehouse, product: Product) -> Stock:

        return Stock.objects.create(
            warehouse=warehouse,
            product=product,
        )

    def _create_transaction(
        self,
        *,
        stock,
        transaction_type,
        quantity,
        user,
        reference="",
        description="",
    ):

        return InventoryTransaction.objects.create(
            stock=stock,
            transaction_type=transaction_type,
            quantity=quantity,
            user=user,
            reference=reference,
            description=description,
        )

    def receive_product(
        self,
        *,
        warehouse: Warehouse,
        product: Product,
        quantity: Decimal,
        user,
        reference: str = "",
        description: str = "",
    ):

        with transaction.atomic():

            self._validate_quantity(quantity)
            self._validate_product(product)
            self._validate_warehouse(warehouse)

            stock = self._get_stock(
                warehouse=warehouse,
                product=product,
            )

            if stock is None:
                stock = self._create_stock(
                    warehouse=warehouse,
                    product=product,
                )

            stock.increase(quantity)

            stock.save(
                update_fields=[
                    "quantity",
                    "updated_at",
                ]
            )

            return self._create_transaction(
                stock=stock,
                transaction_type=InventoryTransaction.TransactionType.IN,
                quantity=quantity,
                user=user,
                reference=reference,
                description=description,
            )

    def issue_product(
        self,
        *,
        warehouse,
        product,
        quantity: Decimal,
        user,
        reference: str = "",
        description: str = "",
    ):

        with transaction.atomic():

            self._validate_quantity(quantity)
            self._validate_product(product)
            self._validate_warehouse(warehouse)

            stock = self._get_locked_stock(warehouse, product)

            stock.decrease(quantity)

            stock.save(
                update_fields=[
                    "quantity",
                    "updated_at",
                ]
            )

            return self._create_transaction(
                stock=stock,
                transaction_type=InventoryTransaction.TransactionType.OUT,
                quantity=quantity,
                user=user,
                reference=reference,
                description=description,
            )

    # race condition NOT Applyed
    def transfer_product(
        self,
        *,
        source_warehouse,
        destination_warehouse,
        product,
        quantity: Decimal,
        user,
        reference: str = "",
        description: str = "",
    ):

        with transaction.atomic():

            self._validate_quantity(quantity)

            self._validate_product(product)

            self._validate_warehouse(source_warehouse)
            self._validate_warehouse(destination_warehouse)

            self._validate_transfer_warehouses(source_warehouse, destination_warehouse)

            source_stock = self._get_stock(
                warehouse=source_warehouse,
                product=product,
            )

            source_stock.decrease(quantity)

            source_stock.save(
                update_fields=[
                    "quantity",
                    "updated_at",
                ]
            )

            destination_stock = self._get_stock(
                warehouse=destination_warehouse,
                product=product,
            )

            if destination_stock is None:
                destination_stock = self._create_stock(
                    warehouse=destination_warehouse,
                    product=product,
                )

            destination_stock.increase(quantity)

            destination_stock.save(
                update_fields=[
                    "quantity",
                    "updated_at",
                ]
            )

            self._create_transaction(
                stock=source_stock,
                transaction_type=InventoryTransaction.TransactionType.OUT,
                quantity=quantity,
                user=user,
                reference=reference,
                description=(f"Transfer to {destination_warehouse.name}"),
            )

            return self._create_transaction(
                stock=destination_stock,
                transaction_type=InventoryTransaction.TransactionType.IN,
                quantity=quantity,
                user=user,
                reference=reference,
                description=(f"Transfer from {source_warehouse.name}"),
            )
