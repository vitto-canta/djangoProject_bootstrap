from django.urls import path

from . import views

urlpatterns = [
    path('search/', views.search, name='search'),
    path('saved/', views.save_unsaved_product, name='save-unsaved-product'),
    path('<slug:category_slug>/<slug:product_slug>/<int:product_id>/', views.product, name='product'),
]
