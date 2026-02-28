from django import forms
from django.db import transaction

from .models import Wallet, Transaction, TransactionCategory
from .other import wallet_balance

class CreateWalletUserForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        
    def clean_name(self):
        name = self.cleaned_data['name']
        if Wallet.objects.filter(user=self.user, name=name).exists():
            raise forms.ValidationError('У вас уже есть кошелек с таким названием!')
        return name
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.user = self.user
        if commit:
            user.save()
        return user
    
    class Meta:
        model = Wallet
        fields = ['name', 'balance', 'currency']
        
class UpdateWalletUserForm(forms.ModelForm):
    class Meta:
        model = Wallet
        fields = ['name', 'balance', 'currency']
        labels = {
            'name': 'Название кошелька',
            'balance': 'Баланс',
            'currency': 'Валюта'
        }
        
class CreateTransactionCategoryForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        
    def clean_name(self):
        name = self.cleaned_data['name']
        if TransactionCategory.objects.filter(user=self.user, name=name).exists():
            raise forms.ValidationError('У вас уже есть такая категория!')
        return name

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user = self.user
        if commit:
            user.save()
        return user
    
    class Meta:
        model = TransactionCategory
        fields = ['name']
    
class UpdateTransactionCategoryForm(forms.ModelForm):
    class Meta:
        model = TransactionCategory
        fields = ['name']
        labels = {
            'name': 'Название категории'
        }
        
class CreateTransactionForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields['wallet'].queryset = Wallet.objects.filter(user=user)
        
    def save(self, commit=True):
        
        trans = super().save(commit=False)
        trans.user = self.user
        
        if not self.is_valid():
            print('Форма не валидна')
            raise ValueError('Форма не валидна, невозможно сохранить')
        
        amount = self.cleaned_data.get('amount')
        transaction_type = self.cleaned_data.get('type')
        
        if commit:
            with transaction.atomic():
                trans.save()
                new_balance = wallet_balance(
                    transaction_obj=trans,
                    new_amount=amount,
                    new_type=transaction_type,
                    operation='create'
                )
                if new_balance is None:
                    raise Exception('Не удалось обновить баланс кошелька')
        return trans
    
    class Meta:
        model = Transaction
        fields = ['type', 'wallet', 'amount', 'category', 'date', 'description']
        widgets = {
            'description': forms.Textarea(attrs={
                'class': 'description-input',
                'placeholder': 'Введите описание транзакции...',
                'rows': 4,
            })
        }
        
class UpdateTransactionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.old_amount = self.instance.amount
            self.old_type = self.instance.type
            
    def save(self, commit=True):
        if not self.is_valid():
            raise ValueError('Форма не валидна')
        
        trans = super().save(commit=False)
        
        if commit:
            with transaction.atomic():
                trans.save()
                new_balance = wallet_balance(
                    transaction_obj=trans,
                    old_amount=self.old_amount,
                    old_type=self.old_type,
                    new_amount=trans.amount,
                    new_type=trans.type,
                    operation='edit'
                )
                if new_balance is None:
                    raise Exception('Не удалось обновить баланс при редоктировании')
            return trans
        
    class Meta:
        model = Transaction
        fields = ['type', 'wallet', 'amount', 'category', 'date', 'description']