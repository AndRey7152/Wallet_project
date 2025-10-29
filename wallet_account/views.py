import logging
from django import forms
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User

from .forms import CreateUserForms, LoginForm

# Create your views here.
def home_view(request):
    details = User.objects.all()
    return render(request, 'wallet/detail/home.html', {'details': details})

def signup_view(request):
    if request.user.is_authenticated:
        return redirect(to='/account/home')
    
    if request.method == 'POST':
        form = CreateUserForms(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Аккаунт с адресом {user.email} создан')
            return redirect(to='/account/home')
    else:
        form = CreateUserForms()
    
    return render(request, 'wallet/register/signup.html', {'form': form})
        
def login_view(request):
    if request.user.is_authenticated:
        return redirect(to='/account/home')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            try:
                user = User.objects.get(email=email)
                user = authenticate(request, username=user.username, password=password)
            except User.DoesNotExist:
                user = None
                
            if user is not None:
                login(request, user)
                if not form.cleaned_data['remember_me']:
                        request.session.set_expiry(0)
            else:
                messages.error(request, 'неверный email или пароль')
            return redirect(to='/account/home')
    else:
        form = LoginForm()
    return render(request, 'wallet/register/login.html', {'form': form})

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'Вы вышли из аккаунта')
    else:
        messages.success(request, 'Вы не были авторизированы')
    return redirect(to='/account/home')