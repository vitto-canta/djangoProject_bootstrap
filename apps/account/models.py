from django.contrib.auth import get_user_model
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin, Permission)
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, username, password, **other_fields):

        other_fields.setdefault('is_vendor', True)
        other_fields.setdefault('is_costumer', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_staff', True)

        if other_fields.get('is_vendor') is not True:
            raise ValueError(
                'Superuser must be assigned to is_vendor=True.')
        if other_fields.get('is_costumer') is not True:
            raise ValueError(
                'Superuser must be assigned to is_costumer=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self._create_user(email, username, password, **other_fields)

    def _create_user(self, email, username, password, is_vendor, is_costumer, is_superuser, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        if not username:
            raise ValueError(_('You must provide a username'))

        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(email=email,
                          username=username,

                          is_superuser=is_superuser,

                          is_vendor=is_vendor,
                          is_costumer=is_costumer,
                          last_login=now,
                          created=now,
                          **other_fields)
        if not password:
            password = get_user_model().objects.make_random_password()
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, username=None, password=None, is_vendor=False, is_costumer=False,
                    **other_fields):
        return self._create_user(email, username, password, is_vendor, is_costumer, False, **other_fields)


class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(max_length=150, unique=True)
    name = models.CharField(max_length=150, blank=True)
    surname = models.CharField(max_length=150, blank=True)

    # Delivery details
    country = CountryField(blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    postcode = models.CharField(max_length=12, blank=True)
    address_line_1 = models.CharField(max_length=150, blank=True)
    address_line_2 = models.CharField(max_length=150, blank=True)
    town_city = models.CharField(max_length=150, blank=True)
    # User Status
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_vendor = models.BooleanField(default=False)
    is_costumer = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email', ]

    class Meta:
        verbose_name = "Accounts"
        verbose_name_plural = "Accounts"
        ordering = ['-last_login', 'username']

        permissions = (
            ("search_item", "can search item"),
            ("view_item", "can view an item"),
            ("view_rate", "can view review rate"),
            ("be_notified", "can receive notifications"),
            ("sell_item", "can sell item"),
            ("confirm_shipment", "can confirm shipment"),
            ("get_paid", "can get paid"),
            ("view_vendor_admin", "can view vendor admin"),
            ("read_review", "can read reviews"),
            ("buy_item", "can buy item"),
            ("view_costumer_admin", "can view costumer admin"),
            ("confirm_delivery", "can confirm delivery"),
            ("write_review", "can write review"),
            ("save_item", "can save item"),
        )

    def __str__(self):
        return self.username

    def add_perm_vendor(self):
        vendor_user_perm = (
            "can sell item",
            "can confirm shipment",
            "can get paid",
            "can view vendor admin",
            "can read reviews",
        )
        for vendor_user_perm_name in vendor_user_perm:
            permission = Permission.objects.get(name=vendor_user_perm_name)
            self.user_permissions.add(permission)

    def add_perm_costumer(self):
        costumer_user_perm = (
            "can buy item",
            "can view costumer admin",
            "can confirm delivery",
            "can write review",
            "can save item",
            "can read reviews",
        )
        for costumer_user_perm_name in costumer_user_perm:
            permission = Permission.objects.get(name=costumer_user_perm_name)
            self.user_permissions.add(permission)


"""
    def costumer(self):
        if self.is_costumer:
            from apps.costumer.models import Costumer
            return Costumer.objects.get(crated_by=self.pk)
        return False

    def vendor(self):
        if self.is_vendor:
            from apps.vendor.models import Vendor
            return Vendor.objects.get(crated_by=self.pk)
        return False
"""
