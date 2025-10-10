from django.shortcuts import render
from .models import Category
# Create your views here.

def detal_wallet(request):
    details = Category.objects.all()
    return render(request, 'wallet/detail_wallet.html', {'details': details})