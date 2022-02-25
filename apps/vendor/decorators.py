from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test

from apps.vendor.models import Vendor


def vendor_required(view_func=None, redirect_field_name=REDIRECT_FIELD_NAME,
                    login_url='upgrade_vendor'):
    def is_vendor(u):
        return Vendor.objects.filter(created_by=u).exists()

    actual_decorator = user_passes_test(lambda u: u.is_vendor and is_vendor, login_url=login_url,
                                        redirect_field_name=redirect_field_name)
    if view_func:
        return actual_decorator(view_func)
    else:
        return actual_decorator
