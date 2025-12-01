from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib import messages

from .models import Profile
from .other import generate_username_from_email
from .email import create_confirmation_email, update_confirmation_email

class CreateUserForms(forms.ModelForm):
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Пароль', max_length=50, widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повтор пароля', max_length=50, widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']
        
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError('Этот email уже зарегестрирован')
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise ValidationError('Пароли не совпадают!')
        
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = False
        user.username = generate_username_from_email(self.cleaned_data['email'])
        user.set_password(self.cleaned_data['password1'])
        
        if commit:
            try:
                user.save()
                profile = Profile.objects.create(user=user, token_type='activation',)
                token = profile.generate_token()
                create_confirmation_email(user, token)
                
            except Exception as e:
                if user.pk:
                    user.delete()
                raise ValidationError(f'Ошибка при регистрации: {str(e)}')
            
        return user
    
class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput)
    remember_me = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['email', 'password', 'remember_me']
        
class UpdateUserForm(forms.ModelForm):
    
    email = forms.EmailField(required=True)
    username = forms.CharField(required=False)
    first_name = forms.CharField(max_length=55)
    last_name = forms.CharField(max_length=55)
    
    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.original_email = self.instance.email
        else:
            self.original_email = None
            
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError('Это "Имя пользователя" уже занято.')
        return username
    
    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        user = self.instance
        
        current_email = user.email.strip().lower() if user.email else ''
        
        if email == current_email:
            return email
        
        if User.objects.filter(email=email).exclude(pk=user.pk).exists():
            raise forms.ValidationError('Этот Email уже зарегестрирован.')
        
        return email
        
    def save(self, commit=True):
        user = super().save(commit=False)
        profile = user.profile
        
        if 'first_name' in self.changed_data:
            user.first_name = self.cleaned_data['first_name']
            
        if 'last_name' in self.changed_data:
            user.last_name = self.cleaned_data['last_name']
            
        if 'username' in self.changed_data:
            username = self.cleaned_data['username']
            user.username = username if username else self.instance.username
                
        if 'email' in self.changed_data:
            new_email = self.cleaned_data['email']
            
            if new_email != self.original_email:
                profile.email_confirmed = False
                profile.new_email = new_email
                profile.token_type = 'change_email'
                profile.generate_token()
                
                try:
                    update_confirmation_email(self.request, user.profile)
                    messages.info(self.request, 'На новый email отправлено письмо для подтверждения')
                except:
                    messages.error(self.request, 'Не удалось отправить письмо подтверждения')
            
        if commit:
            user.save(update_fields=['first_name', 'last_name', 'username'])
            profile.save()
            
        return user
    
