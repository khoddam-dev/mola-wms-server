class InventoryError(Exception):
    """
    Base exception for inventory module.
    """
    pass


class InvalidQuantityError(InventoryError):
    """
    Raised when quantity is zero or negative.
    """
    pass


class StockNotFoundError(InventoryError):
    """
    Raised when stock record does not exist.
    """
    pass


class InsufficientStockError(InventoryError):
    """
    Raised when available stock is not enough.
    """
    pass


class InactiveWarehouseError(InventoryError):
    """
    Raised when warehouse is inactive.
    """
    pass


class InactiveProductError(InventoryError):
    """
    Raised when product is inactive.
    """
    pass


class SameWarehouseTransferError(InventoryError):
    """
    Raised when source and destination warehouses are the same.
    """
    pass