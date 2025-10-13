from django.db import models

# Create your models here.
class User(models.Model):
    '''Модель пользователей'''
    user_name = models.CharField(max_length=50)
    email = models.EmailField(blank=True, null=True)
    password1 = models.CharField(max_length=50)
    password2 = models.CharField(max_length=50)
    telegram_id = models.CharField(max_length=50, blank=True, null=True)
    create = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['create']
        
    def __str__(self):
        return self.user_name
    