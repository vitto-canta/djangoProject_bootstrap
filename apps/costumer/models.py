from django.db import models

from apps.account.models import Account


class Costumer(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.OneToOneField(Account, related_name='costumer', on_delete=models.CASCADE)

    REQUIRED_FIELDS = ['created_by', ]

    class Meta:
        ordering = ['-created_at', 'name']

    def __str__(self):
        return self.name
