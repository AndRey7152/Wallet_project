from django.shortcuts import render, redirect
from django.contrib.auth import login

from .forms import CreateUserForms

# Create your views here.
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