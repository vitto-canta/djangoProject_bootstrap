from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from apps.costumer.models import Costumer
from apps.vendor.models import Vendor


class Review(models.Model):
    made_by = models.ForeignKey(Costumer, on_delete=models.CASCADE)
    addressed_to = models.ForeignKey(Vendor, related_name='reviews', on_delete=models.CASCADE)
    comment = models.TextField(max_length=250)
    rate = models.IntegerField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)
