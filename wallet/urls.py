from django.urls import path
from . import views

app_name = 'wallet'

urlpatterns = [
    path('', views.wallets_user_view, name='my-wallet'),
    
    path('create-wallet/', views.create_wallet_view, name='create_wallet'),
    path('<int:wallet_id>/update/', views.update_wallet_view, name='update_wallet'),
    path('<int:wallet_id>/delete/', views.delete_wallet_view, name='delete_wallet'),
    
    path('all-category/', views.all_category_view, name='all_category'),
    path('create-category/', views.create_category_view, name='create_category'),
    path('<int:category_id>/update-category/', views.update_category_view, name='update_category'),
    path('<int:category_id>/delete-category/', views.delete_category_view, name='delete_category'),
    
    path('create-transaction/', views.create_transaction_view, name='create_transaction'),
    path('<int:transaction_id>/update-transaction/', views.update_transaction_view, name='update_transaction'),
    path('<int:transaction_id>/delete-transaction/', views.delete_transaction_view, name='delete_transaction'),
]