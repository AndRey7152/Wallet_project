from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='wallet/register/reset_password/password_reset.html',
        email_template_name='wallet/register/reset_password/password_reset_email.html',
        subject_template_name='wallet/register/reset_password/password_reset_subject.txt',
        success_url='/password/reset/done/'
    ), name='password_reset'),
    path('password/reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='wallet/register/reset_password/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='wallet/register/reset_password/password_reset_confirm.html',
        success_url='/reset/done/'
        ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='wallet/register/reset_password/password_reset_complete.html'
    ), name='password_reset_complete'),
]
