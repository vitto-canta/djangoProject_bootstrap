from django.urls import path

from . import views

urlpatterns = [
    path('vendor-admin/', views.vendor_admin, name='vendor_admin'),
    path('add-product/', views.add_product, name='add_product'),
    path('edit-vendor/', views.edit_vendor, name='edit_vendor'),
    path('confirm-shipment/<int:pk>/', views.confirm_shipment, name='confirm_shipment'),
    path('recover_credit/', views.recover_credit, name='recover_credit'),
    path('', views.vendors, name='vendors'),
    path('<int:vendor_id>/', views.vendor, name='vendor'),
]
