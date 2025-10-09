from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from utility.bases.base_model import BaseModel


class CustomUser(AbstractBaseUser, PermissionsMixin, BaseModel):
    phone_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(blank=True, null=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created Time")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated Time")

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []  

    def __str__(self):
        return self.phone_number

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
