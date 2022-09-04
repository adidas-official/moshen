from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.sign_up, name='register'),
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('login/', views.loginleek, name='login'),
    path('market/', views.market, name='market'),
    path('trade/', views.trade, name='trade'),
    path('scontract/', views.scontract, name='scontract'),
    path('finance/', views.finance, name='finance'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('mining/', views.mining, name='mining'),
    path('fund/', views.fund, name='fund'),
]
