from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login1, name='login'),
    path('logout/', views.logout_user, name="logout"),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='loan/aut-unlock.html'),
         name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='loan/aut-unlock1.html'),
         name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='loan/aut-password.html'),
         name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='loan/aut-unlock2.html'),
         name="password_reset_complete"),
]