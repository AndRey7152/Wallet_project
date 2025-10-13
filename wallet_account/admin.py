from django.contrib import admin

from .models import User
# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'email', 'password1', 'telegram_id']
    list_filter = ['user_name', 'create']
    search_fields = ['user_name']
    ordering = ['create']
    