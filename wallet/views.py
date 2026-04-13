from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction as trans
from django.urls import reverse

from .models import Wallet, TransactionCategory, Transaction
from .forms import (CreateWalletUserForm, 
                    UpdateWalletUserForm, 
                    CreateTransactionCategoryForm, 
                    UpdateTransactionCategoryForm, 
                    CreateTransactionForm,
                    UpdateTransactionForm)
from .decorators import wallet_access_required, user_object
from .other import wallet_balance

# Create your views here.

''' Кошельки '''
@wallet_access_required
def wallets_user_view(request):
    ''' Функция выводит все кошельки пользователя '''
    wallets = Wallet.objects.order_by('name')
    transactions = Transaction.objects.all().order_by('-date')[:5]
    return render(request, 'wallet/detail/home.html', {'wallets': wallets,
                                                       'transactions': transactions})

@login_required
def create_wallet_view(request):
    ''' Функция создания кошелька '''
    if request.method == 'POST':
        form = CreateWalletUserForm(user=request.user, data=request.POST)
        if form.is_valid():
            try:
                wallet = form.save()
                messages.success(request, f'Кошелек "{wallet.name}" создан!')
                return redirect('/account/my-wallet')
            except Exception as e:
                messages.error(request, f'Ошибка при создании кошелька!')
    else:
        form = CreateWalletUserForm(user=request.user)
           
    return render(request, 'wallet/money/wallet/create_wallet.html', {'form': form})

@user_object(Wallet, obj_id='wallet_id', url='/my-wallets/')
def page_wallet_transaction_view(request, **kwargs):
    ''' Функция вывода трнзакций по кошельку'''
    wallet = kwargs['object']
    print(kwargs)
    transactions = Transaction.objects.filter(wallet=kwargs['wallet_id']).order_by('-date')
    return render(request, 'wallet/money/wallet/page_wallet_transaction.html', {'wallet': wallet, 'transactions': transactions})

@user_object(Wallet, obj_id='wallet_id', url='/my-wallets/')
def update_wallet_view(request, **kwargs):
    ''' Функция обновления данных на кошельке '''
    wallet = kwargs['object']
    if request.method == 'POST':
        form = UpdateWalletUserForm(request.POST, instance=wallet)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, f'Данные кошелька "{wallet.name}" обновлены!')
                return redirect('/account/my-wallet')
            except Exception as e:
                messages.error(request, f'Ошибка при обновлении кошелька "{wallet.name}"!')
    else:
        form = UpdateWalletUserForm(instance=wallet)
            
    return render(request, 'wallet/money/wallet/update_wallet.html', {'form': form, 'wallet': wallet})

@user_object(Wallet, obj_id='wallet_id', url='/my-wallets/')
def delete_wallet_view(request, **kwargs):
    ''' Функция удаления кошелька'''
    wallet = kwargs['object']
    if request.method == 'POST':
        try:
            wallet.delete()
            messages.success(request, f'Кошелек "{wallet.name}" удален!')
            return redirect('/account/my-wallet')
        except Exception as e:
            messages.error(request, f'Ошибка при удалении кошелька "{wallet.name}"!')
    return render(request, 'wallet/money/wallet/delete_wallet.html', {'wallet': wallet})

''' Категории '''
@login_required
def all_category_view(request):
    ''' Функция вывода всех котегории'''
    categories = TransactionCategory.objects.all().order_by('name')
    return render(request, 'wallet/money/transactions_category/all_category.html', {'categories': categories})

@login_required
def create_category_view(request):
    ''' Функция создания категории для трат'''
    if request.method == 'POST':
        form = CreateTransactionCategoryForm(user=request.user, data=request.POST)
        if form.is_valid():
            try:
                category = form.save()
                messages.success(request, f'Категория "{category.name}" добавлена!')
                return redirect('/account/my-wallet/all-category')
            except Exception as e:
                messages.error(request, f'Ошибка при сохранении категории!')
    else:       
        form = CreateTransactionCategoryForm(user=request.user)
            
    return render(request, 'wallet/money/transactions_category/create_category.html', {'form': form})

@user_object(TransactionCategory, obj_id='category_id', url='/my-wallets/')
def update_category_view(request, **kwargs):
    ''' Функция обновления категории для трат'''
    category = kwargs['object']
    if request.method == 'POST':
        form = UpdateTransactionCategoryForm(request.POST, instance=category)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, f'Категория "{category.name}" обновлена!')
                return redirect('/account/my-wallet/all-category')
            except Exception as e:
                messages.error(request, f'Ошибка при обновлении категории "{category.name}"!')
    else:
        form = UpdateTransactionCategoryForm(instance=category)
            
    return render(request, 'wallet/money/transactions_category/update_category.html', {'form': form, 
                                                                                       'category': category})

@user_object(TransactionCategory, obj_id='category_id', url='/my-wallets/')
def delete_category_view(request, **kwargs):
    ''' Функция удаление категории '''
    category = kwargs['object']
    if request.method == 'POST':
        try:
            category.delete()
            messages.success(request, f'Категория "{category.name}" удалена!')
            return redirect('/account/my-wallet/all-category')
        except Exception as e:
            messages.error(request, f'Ошибка при удалении категории "{category.name}"!')
    return render(request, 'wallet/money/transactions_category/delete_category.html', {'category': category})
        
''' Транзакции '''
@login_required
def all_transaction_view(request):
    '''Функция выводит все транзакции'''
    transactions = Transaction.objects.all().order_by('-date')
    return render(request, 'wallet/money/transaction/all_transaction.html', {'transactions': transactions})

@user_object(Transaction, obj_id='transaction_id', url='/account/my-wallet/all-transaction')       
def page_transaction_view(request, **kwargs):
    '''Функция показывает всю информацию о транзакции'''
    transaction = kwargs['object']

    next_url = request.GET.get('next')

    if not next_url:
        next_url = request.session.get('transaction_source')
        if 'transaction_source' in request.session:
            del request.session['transaction_source']
        
    if not next_url:
        next_url = '/account/my-wallet/all-transaction'

    context = {
        'back_url': next_url,
        'transaction': transaction
    }
    print('Рендорится шаблон просмотра страницы транзакции')
    return render(request, 'wallet/money/transaction/page_transaction.html', context)

@login_required
def create_transaction_view(request, wallet_id = None):
    '''Функциия добавления транзакции с опцией привязки к кошельку'''
    wallet = None
    if wallet_id:
        try:
            wallet = Wallet.objects.get(id=wallet_id, user=request.user)
        except Wallet.DoesNotExist:
            messages.error(request, 'Кошелек не найден или у вас нет доступа')
            return redirect('/account/my-wallet/all-transaction')
    
    if request.method == 'POST':
        form = CreateTransactionForm(user=request.user, data=request.POST)
        if form.is_valid():
            try:
                with trans.atomic():
                    transaction = form.save(commit=False)
                    
                if wallet:
                    transaction.wallet = wallet
            
                form.save()
                transaction.user = request.user
                transaction.save()
            
                messages.success(request, f'Транзакция создана!')
            
                if wallet:
                    return redirect(f'/account/my-wallet/{wallet.id}/page-wallet-transaction')
                else:
                    return redirect('/account/my-wallet/all-transaction')
            except Exception as e:
                messages.error(request, 'Ошибка создания транзакции!')
    else:
        form = CreateTransactionForm(user=request.user)
        if wallet:
            form.fields['wallet'].initial = wallet
    return render(request, 'wallet/money/transaction/create_transaction.html', {'form': form})
 
@user_object(Transaction, obj_id='transaction_id', url='/account/my-wallet/all-transaction')       
def update_transaction_view(request, **kwargs):
    ''' Функция обновления транзакций '''
    transaction = kwargs['object']
    if request.method == 'POST':
        form = UpdateTransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Транзакция обновлена!')
                return redirect('/account/my-wallet/all-transaction')
            except Exception as e:
                messages.error(request, 'Ошибка при обновления транзакции!')
    else:
        form = UpdateTransactionForm(instance=transaction)
        
    return render(request, 'wallet/money/transaction/update_transaction.html', {'form': form,
                                                                                'transaction': transaction})
    
@user_object(Transaction, obj_id='transaction_id', url='/account/my-wallet/all-transaction')
def delete_transaction_view(request, **kwargs):
    '''Функция удаления транзакции'''
    transaction = kwargs['object']
    if request.method == 'POST':
        try:
            with trans.atomic():
                new_balance = wallet_balance(
                    transaction_obj=transaction,
                    operation='delete'
                )
                
                if new_balance is None:
                    raise Exception('Не удалось откатить баланс кошелька')
                
            transaction.delete()
            messages.success(request, 'Транзакция удалена!')
            return redirect('/account/my-wallet/all-transaction')
        except Exception as e:
            messages.error(request, 'Ошибка при удалении транзакции!')
            
    return render(request, 'wallet/money/transaction/delete_transaction.html', {'transaction': transaction})