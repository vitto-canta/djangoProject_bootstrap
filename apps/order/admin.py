from django.contrib import admin

from .models import Order, OrderItem


class OrderAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'costumer', 'paid_amount', 'country', 'town_city', 'email']
    list_filter = ['created_at', 'costumer', 'vendors', 'paid_amount', 'town_city']


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'vendor', 'costumer', 'order', 'price', 'quantity', 'status', 'is_reviewed']
    list_filter = ['vendor', 'costumer', 'order', 'price', 'quantity', 'vendor_paid', 'is_shipped', 'is_received',
                   'is_reviewed']


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
