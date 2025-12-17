from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

def wallet_access_required(view_func):
    decorated_view = login_required(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.wallets.exists():
            return redirect(to='create_wallet')
        return decorated_view(request, *args, **kwargs)
    return wrapper