from django.db import models

from apps.account.models import Account


class Vendor(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.OneToOneField(Account, related_name='vendor', on_delete=models.CASCADE)

    REQUIRED_FIELDS = ['created_by', ]

    class Meta:
        ordering = ['-created_at', 'name']

    def __str__(self):
        return self.name

    def get_not_paid_amount(self):
        items = self.seller.filter(vendor_paid=False, order__vendors__in=[self.id])
        return sum((item.product.price * item.quantity) for item in items)

    def get_paid_amount(self):
        items = self.seller.filter(vendor_paid=True, order__vendors__in=[self.id])
        return sum((item.product.price * item.quantity) for item in items)

    def total_gain(self):
        return self.get_not_paid_amount() + self.get_paid_amount()

    def get_average_rate(self):
        reviews = self.reviews.all()
        if len(reviews) > 0:
            return sum(review.rate for review in reviews) / len(reviews)
        else:
            return "no reviews yet"
