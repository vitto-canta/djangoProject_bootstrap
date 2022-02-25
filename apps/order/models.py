from django.db import models
from django_countries.fields import CountryField

from apps.costumer.models import Costumer
from apps.product.models import Product
from apps.vendor.models import Vendor


class Order(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone_number = models.CharField(max_length=15, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_amount = models.DecimalField(max_digits=8, decimal_places=2)
    vendors = models.ManyToManyField(Vendor, related_name='sellers')
    costumer = models.ForeignKey(Costumer, related_name='buyers', on_delete=models.CASCADE)
    costumer_has_paid = models.BooleanField(default=False)
    # Delivery details
    country = CountryField(blank=False)
    postcode = models.PositiveIntegerField(blank=False)
    address_line_1 = models.CharField(max_length=150, blank=False)
    address_line_2 = models.CharField(max_length=150, blank=True)
    town_city = models.CharField(max_length=150, blank=False)

    class Meta:
        ordering = ['-created_at', 'paid_amount']

    def __str__(self):
        return self.name


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='items', on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, related_name='seller', on_delete=models.CASCADE)
    costumer = models.ForeignKey(Costumer, related_name='buyer', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.IntegerField(default=1)
    vendor_paid = models.BooleanField(default=False)
    is_shipped = models.BooleanField(default=False)
    is_received = models.BooleanField(default=False)
    is_reviewed = models.BooleanField(default=False)

    def __str__(self):
        return '%s' % self.id

    def get_total_price(self):
        return self.price * self.quantity

    def status(self):
        if self.is_received:
            return "delivered"
        elif self.is_shipped:
            return "in transit"
        else:
            return "paid"
