from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login

from .models import Category
from .forms import CreateUserForms
# Create your views here.

def home(request):
    posts = Category.objects.all()
    if posts:
       return render(request, 'wallet/detail/home.html', {'posts':posts}) 

def signup_view(request):
    form = CreateUserForms()
    if request.method == 'POST':
        form = CreateUserForms(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('base.html')
        else:
            form = CreateUserForms()
    
    return render(request, 'wallet/register/signup.html', {'form':form})