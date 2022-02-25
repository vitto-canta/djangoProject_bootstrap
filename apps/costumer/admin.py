from django.contrib import admin

from .models import Costumer


class CostumerAdmin(admin.ModelAdmin):
    list_display = ['created_by', 'created_at', 'name']
    list_filter = ['created_at', ]
    search_fields = ['name', 'created_by']


admin.site.register(Costumer, CostumerAdmin)
