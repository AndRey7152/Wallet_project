from django.db import models
from django.utils import timezone
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
    
class Transaction(models.Model):
    TYPE_CHOICES = [
        ('income', 'Доход'),
        ('expense', 'Расход')
    ]
    CATEGORY_CHOICES = []
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    amout = models.DecimalField(max_digits=12, decimal_places=2)
    type = models.CharField(max_length=7, choices=TYPE_CHOICES)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)
    date = models.DateField()
    is_regular = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)