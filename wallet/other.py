from decimal import Decimal

from django.db import transaction
from django.db.models import F

from .models import Wallet, Transaction

def wallet_balance(transaction_obj=None, old_amount=None, old_type=None, new_amount=None, new_type=None, operation='create'):
    '''Функция для работы с балансом кошелька'''
    try:
        with transaction.atomic():
            if operation == 'create':
                wallet = transaction_obj.wallet
                is_income = (new_type == 'income')
                
                if is_income:
                    Wallet.objects.filter(pk=wallet.id).update(balance = F('balance') + Decimal(new_amount))
                else:
                    Wallet.objects.filter(pk=wallet.id).update(balance = F('balance') - Decimal(new_amount))
                    
            elif operation == 'delete':
                wallet = transaction_obj.wallet
                is_income = (transaction_obj.type == 'income')
                
                if is_income:
                    Wallet.objects.filter(pk=wallet.id).update(balance = F('balance') - Decimal(transaction_obj.amount))
                else:
                    Wallet.objects.filter(pk=wallet.id).update(balance = F('balance') + Decimal(transaction_obj.amount))
                
            elif operation == 'edit':
                wallet = transaction_obj.wallet
                old_is_income = (old_type == 'income')
                
                if old_is_income:
                    Wallet.objects.filter(pk=wallet.id).update(balance = F('balance') - Decimal(old_amount))
                else:
                    Wallet.objects.filter(pk=wallet.id).update(balance = F('balance') + Decimal(old_amount))
            
                new_is_income = (new_type == 'income')
                
                if new_is_income:
                    Wallet.objects.filter(pk=wallet.id).update(balance = F('balance') + Decimal(new_amount))
                else:
                    Wallet.objects.filter(pk=wallet.id).update(balance = F('balance') - Decimal(new_amount))
                
        wallet.refresh_from_db()
        return wallet.balance
        
    except (Wallet.DoesNotExist, Transaction.DoesNotExist):
        print(f'Кошелек или транзакция не найден')
        return None
    except (ValueError, TypeError) as e:
        print(f'Ошибка преобразования суммы: {e}')
        return None
    except Exception as e:
        print(f'Непредвиденная ошибка при управлении балансом: {e}')
        return None
