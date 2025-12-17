from django import forms

from .models import Wallet, Transaction

class SignupWalletUserForm(forms.ModelForm):
    name = forms.CharField(
        max_length=100, 
        label='Название кошелька',
        error_messages={'required': 'Укажите название кошелька'}
        )
    balance = forms.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        label='Баланс',
        error_messages={'invalid': 'Введите корректное число'}
        )
    currency = forms.ChoiceField(
        choices=[('RUB', 'Рубль'), ('USD', 'Доллар США'), ('CNY', 'Юань')],
        label='Валюта'
    )
        
    class Meta:
        model = Wallet
        fields = ['name', 'balance', 'currency']
        
class UpdateWalletUserForm(forms.ModelForm):
    name = forms.CharField(max_length=100)
    balance = forms.DecimalField(max_digits=12, decimal_places=2)
    currency = forms.ChoiceField(choices=[('RUB', 'Рубль'), ('USD', 'Доллар США'), ('CNY', 'Юань')])
    
    class Meta:
        model = Wallet
        fields = ['name', 'balance', 'currency']