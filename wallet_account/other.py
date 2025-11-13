import string
import random
import re

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

def generate_username_from_email(email):
    '''Генерация уникального username из email'''
    if not email or '@' not in email:
        raise ValidationError('Некорректный email')
    
    username_base = email.split('@')[0].lower()
    username_base = re.sub(r'[^a-z0-9._-]', '', username_base)
    
    if not username_base:
        username_base = 'user_' + ''.join(random.choices(string.ascii_lowercase, k=6))
    
    max_len = 150
    if len(username_base) > max_len:
        username_base = username_base[:max_len]    
        
    if not User.objects.filter(username=username_base).exists():
        return username_base

    for i in range(1, 10_000):
        candidate = f'{username_base}_{i}'
        if len(candidate) > 150:
            continue
        if not User.objects.filter(username=candidate).exists():
            return candidate
        
        
    raise ValidationError('Не удалось сгенерировать уникальный username')