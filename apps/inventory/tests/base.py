from decimal import Decimal

from django.test import TestCase

from apps.inventory.models import Stock
from apps.warehouse.models import Warehouse
from apps.identity.models import (
    Role,
    User,
)
from apps.core.models import (
    Country,
    Province,
    City,
)
from apps.products.models import (
    Brand,
    Category,
    Product,
    Unit,
)

from apps.inventory.services import InventoryService


class InventoryBaseTest(TestCase):

    def setUp(self):
        self.inventory_service = InventoryService()

    @classmethod
    def setUpTestData(cls):

        cls.country = Country.objects.create(
            code="IRN",
            name="Iran",
        )

        cls.province = Province.objects.create(
            country=cls.country,
            name="Fars",
        )

        cls.city = City.objects.create(
            province=cls.province,
            name="Shiraz",
        )

        cls.role = Role.objects.create(
            name="Administrator",
        )

        cls.user = User.objects.create_user(
            username="admin",
            password="admin",
            first_name="Ali",
            last_name="Khoddam",
            national_code="1234567890",
            mobile="09123456789",
            role=cls.role,
        )

        cls.unit = Unit.objects.create(
            symbol="PCS",
            name="Piece",
        )

        cls.brand = Brand.objects.create(name="Samsung")

        cls.category = Category.objects.create(
            name="Electronics",
        )

        cls.product = Product.objects.create(
            code="SSD001",
            name="Samsung SSD",
            unit=cls.unit,
            brand=cls.brand,
            category=cls.category,
        )

        cls.warehouse = Warehouse.objects.create(
            code="WH001",
            name="Central Warehouse",
            city=cls.city,
        )

        cls.second_warehouse = Warehouse.objects.create(
            code="WH002",
            name="Backup Warehouse",
            city=cls.city,
        )

        cls.stock = Stock.objects.create(
            warehouse=cls.warehouse,
            product=cls.product,
            quantity=Decimal("0"),
        )
