from functools import wraps
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.http import Http404

def wallet_access_required(view_func):
    '''Декоратор проверки наличия кошелька у пользователя для работы с сайтом'''
    @login_required
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(to='login')
        try:
            if not hasattr(request.user, 'wallets') or not request.user.wallets.exists():
                messages.info(request, 'У вас нет кошельков, для работы с сайтом создайте кошелек')
                return redirect('wallet_account:wallet:create_wallet')
        except AttributeError:
            # Если related_name 'wallets' не задан, используем прямой запрос
            from wallet.models import Wallet
            if not Wallet.objects.filter(user=request.user).exists():
                return redirect('create_wallet')
        return view_func(request, *args, **kwargs)
    return wrapper

def user_object(db, obj_id ='id', field='user', url=None):
    ''' Декоратор для проверки принадлежности объекта текущему пользователю '''
    def decorator(view_func):
        @login_required
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            obj = kwargs.get(obj_id)
            redirect_to = url or request.META.get('HTTP_REFFERER', '/')
            if not obj:
                messages.error(request, f'Не указан ID объекта {obj_id}')
                return redirect(redirect_to)
            
            try:
                obj = get_object_or_404(db, **{'id':obj, field:request.user})
            except Http404:
                messages.error(request, 'У вас нет доступа к этому объекту')
                return redirect(redirect_to)
            
            kwargs['object'] = obj
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator