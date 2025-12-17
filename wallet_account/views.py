import logging

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.core.validators import validate_email
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import PasswordChangeView
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import transaction

from wallet.models import Wallet
from .models import Profile
from .forms import CreateUserForms, LoginForm, UpdateUserForm

# Create your views here.
def home_view(request):
    '''Главная страница'''
    return render(request, 'wallet/detail/home.html')

def signup_view(request):
    '''Функция регистрации пользователя'''
    if request.user.is_authenticated:
        return redirect(to='/account/my-wallet')
    
    if request.method == 'POST':
        form = CreateUserForms(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            
            try:
                user = User.objects.get(email=email)
                
                if user.is_active == False:
                    user.is_active = True
                    user.set_password(form.cleaned_data['password1'])
                    user.save()
                    login(request, user)
                    return redirect(to='/account/home')
                else:
                    messages.error(request, 'Пользователь с таким email уже зарегестрирован')
            except User.DoesNotExist:
                user = form.save()
                login(request, user)
                messages.success(request, f'Аккаунт с адресом {user.email} создан')
                return redirect(to='/account/home')
    else:
        form = CreateUserForms()
    
    return render(request, 'wallet/register/signup.html', {'form': form,
                                                            'wallets': Wallet.objects.filter(user=request.user)})
        
def login_view(request):
    '''Функция входа в аккаунт'''
    if request.user.is_authenticated:
        return redirect(to='/account/my-wallet')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            try:
                user = User.objects.get(email=email)
                
                if not user.is_active:
                    messages.error(request, 'Аккаунт пользователя не найден.')
                    return render(request, 'wallet/register/login.html', {'form': form})
                
                user = authenticate(request, username=user.username, password=password)
            except User.DoesNotExist:
                messages.error(request, 'Пользователь с таким email не найден')
                return render(request, 'wallet/register/login.html', {'form': form})
                
            if user is not None:
                login(request, user)
                if not form.cleaned_data['remember_me']:
                        request.session.set_expiry(0)
            else:
                messages.error(request, 'Неверный пароль')
                return render(request, 'wallet/register/login.html', {'form': form})
            return redirect(to='/account/my-wallet')
    else:
        form = LoginForm()
    return render(request, 'wallet/register/login.html', {'form': form})

def logout_view(request):
    '''Функция выхода из аккаунта пользователя'''
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'Вы вышли из аккаунта')
    else:
        messages.success(request, 'Вы не были авторизированы')
    return redirect(to='/account/home')

def confirm_email(request, token):
    '''Подтверждение email и обновление адреса'''
    try:
        profile = get_object_or_404(Profile, confirmate_token=token)
        
        if not profile.token_expires or profile.token_expires < timezone.now():
            messages.error(request, 'Ссылка устарела. Запросите новое подтверждение.')
            profile.invalidate_token()
            return redirect(to='/account/home')
            
        user = profile.user
        new_email = profile.new_email
        
        with transaction.atomic():
            
            if profile.token_type == 'activation':
                if not user.email:
                    messages.success('')
        
                try:
                    validate_email(user.email)
                except ValidationError:
                    messages.error(request, 'Некорректный email аккаунта')
                    profile.invalidate_token()
                    return redirect(to='/account/home')
                
                user.is_active = True
                user.save()
                messages.success(request, 'Аккаунт активирован!')
        
            elif profile.token_type == 'change_email':
                
                if not new_email:
                    messages.error(request, 'Аккаунт активирован! Можно войти')
                    profile.invalidate_token()
                    return redirect(to='/account/my-wallet')
                
                try:
                    validate_email(new_email)
                except ValidationError:
                    messages.error(request, 'Некорректный формат email')
                    profile.invalidate_token()
                    return redirect(to='/account/home')
                
                if User.objects.filter(email=profile.new_email).exclude(pk=user.pk).exists():
                    messages.error(request, 'Этот email уже зарегестрирован')
                    profile.invalidate_token()
                    return redirect(to='/account/home')
        
                user.email = new_email
                user.save()
                #print(f'Email изменен: {old_email} > {new_email}')
                
            profile.invalidate_token()
            profile.email_confirmed = True
            profile.save()
        
        messages.success(request, 'Email успешно подтвержден и обновлен')
        return redirect(to='/account/home')
        
    except Profile.DoesNotExist:
        messages.error(request, 'Неверная ссылка активации!')
    except Exception as e:
        messages.error(request, f'Произошла ошибка: {str(e)}')
    return redirect(to='/account/home')
    
    
def update_user_view(request):
    ''' Обновление профиля '''
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=request.user)
        form.request = request
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Профиль успешно обновлен')
            return redirect(to='/account/my-wallet')
    else:
        form = UpdateUserForm(instance=request.user)
    return render(request, 'wallet/register/update_user.html', {'form': form, 
                                                                'wallets': Wallet.objects.filter(user=request.user)})

def delete_user_view(request):
    ''' Удаление аккаунта '''
    if request.method == 'GET':
        try:
            user = User.objects.get(username = request.user.username)
            user.is_active = False
            user.save()
            return redirect(to='/account/home')
        except User.DoesNotExist:
            pass
    return render(request, 'wallet/register/delete_user.html')

class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    ''' Изменение пароля '''
    template_name = 'wallet/register/reset_password/change_password.html'
    success_message = 'Пароль успешно изменен.'
    success_url = reverse_lazy('wallet_account:my_wallet')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            context['wallets'] = Wallet.objects.filter(user=self.request.user)
        else:
            context['wallets'] = []
            
        return context