from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Wallet(models.Model):
    '''Кошелек пользователя'''
    name = models.CharField(max_length=40)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    user_id = models.ForeignKey(User, 
                                on_delete=models.CASCADE)
    class Meta:
        ordering = ['name', 'amount',]
        
    def __str__(self):
        return self.name
    
class Category(models.Model):
    '''Категория трат'''
    name = models.CharField(max_length=100)
    
    class Meta:
        ordering = ['name',]
    
    def __str__(self):
        return self.name
    
class Transactions(models.Model):
    '''Траты пользователя по категориям'''
    class Status(models.TextChoices):
        INCOME = 'Доход',
        EXPENSE = 'Расход'
        
    user = models.ForeignKey(User,
                                on_delete=models.CASCADE,)
    category = models.ForeignKey(Category, 
                                 on_delete=models.CASCADE,)
    wallet_transact = models.ForeignKey(Wallet, 
                                        on_delete=models.CASCADE)
    type = models.CharField(max_length=7, choices=Status.choices, default=Status.EXPENSE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-date',]
        
    def __str__(self):
        return self.type
    
    def save(self, *args, **kwargs):
        if self.wallet_transact is None:
            try:
                default_wallet = Wallet.objects.first()
                if default_wallet:
                    self.wallet_transact = default_wallet
            except Wallet.DoesNotExist:
                pass
        super().save(*args, **kwargs)    
