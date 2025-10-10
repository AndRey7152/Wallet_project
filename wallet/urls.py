from django.urls import path
from . import views

app_name = 'wallet'

urlpatterns = [
    path('detail/', views.detal_wallet, name='detail_wallet')
]