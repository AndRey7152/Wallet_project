from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from .models import Wallet, Transaction
from .forms import SignupWalletUserForm, UpdateWalletUserForm
from .decorators import wallet_access_required

# Create your views here.

@wallet_access_required
def wallets_user_view(request):
    wallets = Wallet.objects.all()
    return render(request, 'wallet/detail/home.html', {'wallets': wallets})

@wallet_access_required
def create_wallet_view(request):
    if request.method == 'POST':
        form = SignupWalletUserForm(request.POST)
        if form.is_valid():
            wallet = form.save(commit=False)
            wallet.user = request.user
            wallet.save()
        return redirect(to='/account/my-wallet')
    else:
        form = SignupWalletUserForm()
            
    return render(request, 'wallet/money/create_wallet.html', {'form': form})

@wallet_access_required
def update_wallet_view(request, wallet_id):
    wallet = get_object_or_404(Wallet, id=wallet_id, user=request.user)
    if request.method == 'POST':
        form = UpdateWalletUserForm(request.POST, instance=wallet)
        if form.is_valid():
            form.save()
            messages.success(request, 'Данные кошелька обновлены!')
            return redirect(to='/account/my-wallet', wallet_id=wallet.id)
    else:
        form = UpdateWalletUserForm(instance=wallet)
    return render(request, 'wallet/money/update_wallet.html', {'form': form, 'wallet': wallet})

@wallet_access_required
def delete_wallet_view(request, wallet_id):
    wallet = get_object_or_404(Wallet, id=wallet_id, user=request.user)
    if request.method == 'GET':
        wallet.delete()
        messages.success(request, 'Кошелек удален')
        return redirect(to='/account/my-wallet')
    return render(request, 'wallet/money/delete_wallet.html', {'wallet': wallet})