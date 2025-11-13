import logging

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse

from .models import Profile
from .forms import CreateUserForms, LoginForm, UpdateUserForm

# Create your views here.
def home_view(request):
    details = Profile.objects.all()
    return render(request, 'wallet/detail/home.html', {'details': details})

def signup_view(request):
    '''Функция регистрации пользователя'''
    if request.user.is_authenticated:
        return redirect(to='/account/home')
    
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
    
    return render(request, 'wallet/register/signup.html', {'form': form})
        
def login_view(request):
    '''Функция входа в аккаунт'''
    if request.user.is_authenticated:
        return redirect(to='/account/home')
    
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
            return redirect(to='/account/home')
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
    '''Подтверждение email'''
    try:
        profile = get_object_or_404(Profile, confirmate_token=token)
        user = profile.user
        user.is_active = True
        user.save()
        
        profile.invalidate_token()
        profile.email_confirmed = True
        profile.save()
        
        return HttpResponse('Email подтвержден!')
    except Profile.DoesNotExist:
        return HttpResponse('Неверная ссылка активации!')
    
    
def update_user_view(request):
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            return redirect(to='/account/home')
    else:
        form = UpdateUserForm(instance=request.user)
    return render(request, 'wallet/register/update_user.html', {'form': form})

def delete_user_view(request):
    if request.method == 'GET':
        try:
            user = User.objects.get(username = request.user.username)
            user.is_active = False
            user.save()
            return redirect(to='/account/home')
        except User.DoesNotExist:
            pass
    return render(request, 'wallet/register/delete_user.html')