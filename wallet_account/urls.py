from django.urls import path, include

from . import views

app_name = 'wallet_account'

urlpatterns = [
    path('home/', views.home_view, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('update-user/', views.update_user_view, name='update_user'),
    path('delete-user/', views.delete_user_view, name='delete_user'),
    path('confirm-email/<str:token>/', views.confirm_email, name='confirm_email'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('', include('wallet_account.urls_password')),
    path('my-wallet/', include('wallet.urls')),
] 