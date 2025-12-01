import uuid

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Profile(models.Model):
    
    TOKEN_TYPE_CHOICES = [
        ('activateion', 'Активация аккаунта'),
        ('change_email', 'Сиена email'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    new_email = models.EmailField(blank=True, null=True)
    email_confirmed = models.BooleanField(default=True)
    confirmate_token = models.CharField(max_length=36, unique=True, null=True, blank=True)
    token_expires = models.DateTimeField(null=True, blank=True)
    telegram_id = models.CharField(max_length=50, blank=True, null=True)
    token_type = models.CharField(max_length=20, choices=TOKEN_TYPE_CHOICES, default='activation')
    
    
    def generate_token(self):
        self.confirmate_token = str(uuid.uuid4())
        self.token_expires = timezone.now() + timezone.timedelta(hours=24)
        self.save()
        return self.confirmate_token
    
    def invalidate_token(self):
        self.new_email = None
        self.confirmate_token = None
        self.token_expires = None
        self.save()
        
