from utility.bases.base_model import BaseModel

from django.db import models

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from account.models.managers.custom_user_manager import CustomUserManager



class CustomUser(AbstractBaseUser, PermissionsMixin, BaseModel):
    phone_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(blank=True, null=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created Time")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated Time")

    is_email_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['password']  # فیلدهایی که هنگام createsuperuser باید پر شن (مثل first_name, last_name و غیره)

    objects = CustomUserManager()  

    def __str__(self):
        return self.phone_number

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
