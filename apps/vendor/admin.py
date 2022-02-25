from django.contrib import admin

from .models import Vendor


class VendorAdmin(admin.ModelAdmin):
    list_display = ['created_by', 'created_at', 'name', 'get_paid_amount', 'get_not_paid_amount', 'total_gain',
                    'get_average_rate']
    list_filter = ['created_at', ]
    search_fields = ['name', 'created_by']


admin.site.register(Vendor, VendorAdmin)
