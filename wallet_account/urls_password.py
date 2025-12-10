from django.urls import path, include
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='wallet/register/reset_password/password_reset.html',
        email_template_name='wallet/register/reset_password/password_reset_email.html',
        subject_template_name='wallet/register/reset_password/password_reset_subject.txt',
        success_url=reverse_lazy('wallet_account:password_reset_done')
    ), name='password_reset'),
    path('password/reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='wallet/register/reset_password/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='wallet/register/reset_password/password_reset_confirm.html',
        success_url=reverse_lazy('wallet_account:password_reset_complete')
        ), name='password_reset_confirm'),
    path('password/reset/complete', auth_views.PasswordResetCompleteView.as_view(
        template_name='wallet/register/reset_password/password_reset_complete.html'
    ), name='password_reset_complete'),
]
