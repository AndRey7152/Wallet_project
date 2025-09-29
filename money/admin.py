from django.contrib import admin
from .models import User, Category, Transactions

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'money', 'email', 'telegram_id']
    list_filter = ['user_name', 'create']
    search_fields = ['user_name', 'telegram_id']
    ordering = ['create']
    
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    ordering = ['name']
    
@admin.register(Transactions)
class TransactionsAdmin(admin.ModelAdmin):
    list_display = ['user', 'category', 'type', 'amount', 'description', 'date']
    list_filter = ['category', 'type', 'amount', 'date']
    search_fields = ['category']
    raw_id_fields = ['user', 'category']
    date_hierarchy = 'date'
    ordering = ['date']