from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login1, name='login'),
    path('logout/', views.logout_user, name="logout"),
    path('register/', views.register, name="register"),
    path('reset_password/', views.send_reset, name="send_reset"),
    path('reset_password/<int:pk>/<str:token>/', views.new_password, name="new_password"),
    path('customers/', views.customers, name="customers"),
    path('update_customer/<int:pk>/', views.update_customer, name="update_customer"),
    path('delete_customer/<int:pk>/', views.delete_customer, name="delete_customer"),
    ]