from django.urls import path
from . import views

app_name = 'wallet'

urlpatterns = [
    path('', views.wallets_user_view, name='my-wallet'),
    path('create-wallet/', views.create_wallet_view, name='create_wallet'),
    path('<int:wallet_id>/update/', views.update_wallet_view, name='update_wallet'),
    path('<int:wallet_id>/delete/', views.delete_wallet_view, name='delete_wallet'),
]