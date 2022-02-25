from django.contrib import admin

from .models import Category, Product


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'ordering']
    list_filter = ['ordering']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'vendor', 'price', 'date_added', 'is_sold', 'quantity']
    list_filter = ['category', 'vendor', 'is_sold', 'price', 'date_added']
    search_fields = ['title', 'description']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
