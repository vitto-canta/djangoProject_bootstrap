from django.urls import path

from apps.review import views

urlpatterns = [

    path('leave-review/<int:pk>/', views.leave_review, name='leave_review'),

]
