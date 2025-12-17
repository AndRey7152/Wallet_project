def user_wallets(request):
    if request.user.is_authenticated:
        return {
            'user_wallets': request.user.wallets.all(),
            'has_active_wallets': request.user.wallets.exists()
        }
    return {}