from django.urls import path

from apps.costumer import views

urlpatterns = [
    path('costumer-admin/', views.costumer_admin, name='costumer_admin'),
    path('edit-costumer/', views.edit_costumer, name='edit_costumer'),
    path('confirm-delivery/<int:pk>/', views.confirm_delivery, name='confirm_delivery'),

]
