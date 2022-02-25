"""fleamarket URL Configuration
"""
import notifications.urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('vendors/', include('apps.vendor.urls')),
                  path('cart/', include('apps.cart.urls')),
                  path('costumers/', include('apps.costumer.urls')),
                  path('account/', include('apps.account.urls')),
                  path('products/', include('apps.product.urls')),
                  path('review/', include('apps.review.urls')),
                  path('inbox/notifications', include(notifications.urls, namespace='notifications')),
                  path('', include('apps.core.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
