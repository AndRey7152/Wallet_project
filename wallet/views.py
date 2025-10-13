from django.shortcuts import render

from .models import Category
# Create your views here.

def home(request):
    posts = Category.objects.all()
    if posts:
       return render(request, 'wallet/detail/home.html', {'posts':posts}) 

