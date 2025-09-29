import datetime

from django.db import models

# Create your models here.

class User(models.Model):
    '''Модель пользователей'''
    user_name = models.CharField(max_length=50)
    money = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    email = models.EmailField(blank=True)
    telegram_id = models.CharField(max_length=10, blank=True)
    create = models.DateTimeField(auto_now_add=True)
    
    
    class Meta:
        ordering = ['user_name', 'money', 'email', 'telegram_id']
        
    def __str__(self):
        return self.user_name
    
class Category(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class Transactions(models.Model):
    class Status(models.TextChoices):
        INCOME = 'Доход',
        EXPENSE = 'Расход'
    user = models.ForeignKey(User,
                                on_delete=models.CASCADE,)
    category = models.ForeignKey(Category, 
                                 on_delete=models.CASCADE,
                                 )
    type = models.CharField(max_length=7, choices=Status.choices, default=Status.EXPENSE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    description = models.TextField(blank=True)
    
    class Meta:
        ordering = ['date']
    