from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test

from apps.costumer.models import Costumer


def costumer_required(view_func=None, redirect_field_name=REDIRECT_FIELD_NAME,
                      login_url='upgrade_costumer'):
    def is_costumer(u):
        return Costumer.objects.filter(created_by=u).exists()

    actual_decorator = user_passes_test(lambda u: u.is_costumer and is_costumer, login_url=login_url,
                                        redirect_field_name=redirect_field_name)
    if view_func:
        return actual_decorator(view_func)
    else:
        return actual_decorator
