from django.urls import path
from . import views

app_name = 'wallet'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('loggin/', views.signup_view, name='signup_view'),
]