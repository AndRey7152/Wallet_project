import datetime

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Wallet(models.Model):
    CURRENCY_CHOICES = [
        ('RUB', 'Рубль'),
        ('USD', 'Доллар США'),
        ('CNY', 'Юань')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wallets')
    name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=12, decimal_places=2,default=0)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='RUB')
    is_active = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    def get_currency_icon(self):
        '''Возвращает иконку валюты по ее коду'''
        icons = {
            'RUB': '₽',
            'USD': '$',
            'CNY': '¥',
        }
        return icons.get(self.currency, '₽')
    
    def __str__(self):
        return self.name
    
class TransactionCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название категории')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    create_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    class Meta:
        unique_together = ('user', 'name')
        

class Transaction(models.Model):
    TYPE_CHOICES = [
        ('income', 'Доход'),
        ('expense', 'Расход')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    type = models.CharField(max_length=7, choices=TYPE_CHOICES, default='Доход')
    category = models.ForeignKey(TransactionCategory, on_delete=models.SET_NULL, null=True)
    description = models.TextField(blank=True)
    date = models.DateField(default=datetime.datetime.now, editable=True)
    is_regular = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)
    
    def get_type_translate(self):
        type = {
            'income': 'Доход',
            'expense': 'Расход'
        }
        return type.get(self.type, 'Расход')