from decimal import Decimal

from django.db import transaction

from apps.inventory.exceptions import (
    StockNotFoundError,
    InactiveProductError,
    InactiveWarehouseError,
    SameWarehouseTransferError,
)

from apps.inventory.models import (
    InventoryTransaction,
    Stock,
)

class InventoryService:

    def _get_stock(
        self,
        *,
        warehouse,
        product,
    ):
        try:
            return Stock.objects.get(
                warehouse=warehouse,
                product=product,
            )

        except Stock.DoesNotExist:
            raise StockNotFoundError(
                "Stock record not found."
            )
    
    def _get_or_create_stock(
        self,
        *,
        warehouse,
        product,
    ):
        stock, _ = Stock.objects.get_or_create(
            warehouse=warehouse,
            product=product,
            defaults={
                "quantity": 0,
            },
        )

        return stock

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
        warehouse,
        product,
        quantity: Decimal,
        user,
        reference: str = "",
        description: str = "",
    ):

        with transaction.atomic():

            if not warehouse.is_active:
                raise InactiveWarehouseError(
                    "Warehouse is inactive."
                )

            if not product.is_active:
                raise InactiveProductError(
                    "Product is inactive."
                )

            stock = self._get_or_create_stock(
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

            transaction_record = self._create_transaction(
                stock=stock,
                transaction_type=InventoryTransaction.TransactionType.IN,
                quantity=quantity,
                user=user,
                reference=reference,
                description=description,
            )

            return transaction_record

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

            if not warehouse.is_active:
                raise InactiveWarehouseError(
                    "Warehouse is inactive."
                )

            if not product.is_active:
                raise InactiveProductError(
                    "Product is inactive."
                )

            stock = self._get_stock(
                warehouse=warehouse,
                product=product,
            )

            stock.decrease(quantity)

            stock.save(
                update_fields=[
                    "quantity",
                    "updated_at",
                ]
            )

            transaction_record = self._create_transaction(
                stock=stock,
                transaction_type=InventoryTransaction.TransactionType.OUT,
                quantity=quantity,
                user=user,
                reference=reference,
                description=description,
            )

            return transaction_record

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

            if source_warehouse == destination_warehouse:
                raise SameWarehouseTransferError(
                    "Source and destination warehouses must be different."
                )
            
            if not source_warehouse.is_active:
                raise InactiveWarehouseError(
                    "Source warehouse is inactive."
                )

            if not destination_warehouse.is_active:
                raise InactiveWarehouseError(
                    "Destination warehouse is inactive."
                )

            if not product.is_active:
                raise InactiveProductError(
                    "Product is inactive."
                )

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


            destination_stock = self._get_or_create_stock(
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
                description=(
                    f"Transfer to {destination_warehouse.name}"
                ),
            )


            transaction_record = self._create_transaction(
                stock=destination_stock,
                transaction_type=InventoryTransaction.TransactionType.IN,
                quantity=quantity,
                user=user,
                reference=reference,
                description=(
                    f"Transfer from {source_warehouse.name}"
                ),
            )


            return transaction_record