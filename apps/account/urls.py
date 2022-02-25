from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import AuthenticationForm
from django.urls import path

from apps.account import views

urlpatterns = [

    path('login/', auth_views.LoginView.as_view(template_name='account/login.html',
                                                form_class=AuthenticationForm, ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/account/login/'), name='logout'),
    path('register/', views.register, name='register'),
    path('upgrade_costumer/', views.upgrade_costumer, name='upgrade_costumer'),
    path('upgrade_vendor/', views.upgrade_vendor, name='upgrade_vendor'),
    path('notifications/', views.notification, name='notifications'),
    path('notifications/update', views.mark_notifications_read, name='mark_notifications_read'),
    path('data/', views.personal_data, name='personal_data'),
    path('change-password/', views.change_password, name='change_password'),
]
