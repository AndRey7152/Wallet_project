from django.contrib import admin
from .models import Category, Transactions, Wallet

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    ordering = ['name']
    
@admin.register(Transactions)
class TransactionsAdmin(admin.ModelAdmin):
    list_display = ['user', 'category',  'type', 'amount', 'description', 'date']
    list_filter = ['category', 'wallet_transact', 'type', 'amount', 'date']
    search_fields = ['category', 'user_id']
    raw_id_fields = ['user', 'category', 'wallet_transact']
    date_hierarchy = 'date'
    ordering = ['-date']
    
    
@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ['name', 'amount', 'user_id']
    list_filter = ['user_id']
    search_fields = ['user_id']
    ordering = ['name', 'amount']
    