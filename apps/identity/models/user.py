from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from apps.core.models import BaseModel
from .role import Role
from .user_manager import UserManager


class User(AbstractBaseUser, PermissionsMixin, BaseModel):

    username = models.CharField(max_length=150, unique=True)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    national_code = models.CharField(max_length=10, unique=True)
    mobile = models.CharField(max_length=11, unique=True)

    role = models.ForeignKey(
        Role,
        on_delete=models.PROTECT,
        related_name="users",
    )

    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "users"
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username
