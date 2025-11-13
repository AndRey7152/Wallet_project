import uuid

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.conf import settings
from django.urls import reverse

from .models import Profile
from .other import generate_username_from_email

class CreateUserForms(forms.ModelForm):
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Пароль', max_length=50, widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повтор пароля', max_length=50, widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['email']
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = False
        user.username = generate_username_from_email(self.cleaned_data['email'])
        user.set_password(self.cleaned_data['password1'])
        
        if commit:
            user.save()
            profile = Profile.objects.create(user=user)
            token = profile.generate_token()
            
            try:
                self.send_confirmation_email(user, token)
            except Exception as e:
                print(f'Ошибка отправки письма. Ошибка: {e}')
            
        return user
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            pass
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise ValidationError('Пароли не совпадают!')
        
        return cleaned_data
    
    
    def send_confirmation_email(self, user, token):
        from django.core.mail import send_mail, get_connection
        link = settings.BASE_URL + reverse('wallet_account:confirm_email', kwargs={'token':token})
        try:
            conection = get_connection(timeout=30)
            send_mail(
                subject='Подтвердите email',
                message=(
                    f'Здравствуйте!\n\n'
                    f'Для активации аккаунта перейдите по ссылке:\n'
                    f'{link}\n\n'
                    'Ссылка действительна 24 часа.\n\n'
                    'Еслиы вы не регистрировались на нашем сайте - проигнорируйте это письмо.'
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                connection=conection,
                fail_silently=False,
            )
        except Exception as e:
            print(f'Ошибка отправки письма пользователю {user.email}: {e}')
            raise
        
    
class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput)
    remember_me = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['email', 'password', 'remember_me']
        
class UpdateUserForm(forms.ModelForm):
    
    username = forms.CharField(required=False)
    first_name = forms.CharField(max_length=55)
    last_name = forms.CharField(max_length=55)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError('Это "Имя пользователя" уже занято.')
        return username
        
    def save(self, commit=True):
        user = super().save(commit=False)
        
        if self.cleaned_data['first_name']:
            user.first_name = self.cleaned_data['first_name']
        if self.cleaned_data['last_name']:
            user.last_name = self.cleaned_data['last_name']
            
        if not self.cleaned_data['username']:
            user.username = self.changed_data['username']
            
        if commit:
            user.save()
        return user