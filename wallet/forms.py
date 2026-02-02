from django import forms

from .models import Wallet, Transaction, TransactionCategory

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
        self.user = user
        super().__init__(*args, **kwargs)
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.user = self.user
        if commit:
            user.save()
        return user
    
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
    class Meta:
        model = Transaction
        fields = ['type', 'wallet', 'amount', 'category', 'date', 'description']