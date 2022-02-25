from django.contrib import admin

from apps.account.models import Account


class AccountAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_vendor', 'is_costumer', 'created', 'last_login']
    list_filter = ['created', 'last_login', 'is_vendor', 'is_costumer']
    search_fields = ['username', 'email', 'name', 'surname']


admin.site.register(Account, AccountAdmin)
