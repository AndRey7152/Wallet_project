import uuid

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)
    confirmate_token = models.CharField(max_length=36, unique=True, null=True, blank=True)
    telegram_id = models.CharField(max_length=50, blank=True, null=True)
    
    
    def generate_token(self):
        self.confirmate_token = str(uuid.uuid4())
        self.save()
        return self.confirmate_token
    
    def invalidate_token(self):
        self.confirmate_token = None
        self.save()