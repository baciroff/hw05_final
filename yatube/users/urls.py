from django.contrib.auth.views import (LoginView, LogoutView,
                                       PasswordChangeDoneView,
                                       PasswordResetCompleteView,
                                       PasswordResetConfirmView,
                                       PasswordResetDoneView,
                                       PasswordResetView)
from django.urls import path, reverse_lazy

from . import views

app_name = 'users'


urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('login/',
         LoginView.as_view(template_name='users/login.html'),
         name='login'),
    path('logout/',
         LogoutView.as_view(template_name='users/logged_out.html'),
         name='logout'),
    path('password_reset/',
         PasswordResetView.as_view(success_url=reverse_lazy(
             'users:password_reset_done'),
             template_name="users/password_reset_form.html"),
         name='password_reset'),
    path('password_reset/done',
         PasswordResetDoneView.as_view(
             template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('password_reset/confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(
             template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password_reset/complete',
         PasswordResetCompleteView.as_view(
             template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
    path('password_change',
         views.PasswordChange.as_view(),
         name='password_change_form'),
    path('password_change/done',
         PasswordChangeDoneView.as_view(
             template_name='users/password_change_done.html'),
         name='password_change_done'),
]
