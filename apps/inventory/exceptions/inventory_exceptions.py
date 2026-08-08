class InventoryError(Exception):
    """
    Base exception for inventory module.
    """

    default_message = "Inventory error."

    def __init__(self, message: str | None = None):
        super().__init__(message or self.default_message)


class InvalidQuantityError(InventoryError):
    """
    Raised when quantity is zero or negative.
    """

    default_message = "Quantity must be greater than zero."


class StockNotFoundError(InventoryError):
    """
    Raised when stock record does not exist.
    """

    default_message = "Stock record not found."


class InsufficientStockError(InventoryError):
    """
    Raised when available stock is not enough.
    """

    default_message = "Insufficient stock."


class InactiveWarehouseError(InventoryError):
    """
    Raised when warehouse is inactive.
    """

    default_message = "Warehouse is inactive."


class InactiveProductError(InventoryError):
    """
    Raised when product is inactive.
    """

    default_message = "Product is inactive."


class SameWarehouseTransferError(InventoryError):
    """
    Raised when source and destination warehouses are the same.
    """

    default_message = "Source and destination warehouses must be different."
