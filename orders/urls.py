
from django.urls import path
from . import views

urlpatterns = [
    path('create-order', views.checkout, name="checkout"),
    path('coin-deposit', views.coinDeposit.as_view(), name="coin_deposit"),
    path('bank-deposit', views.bankDeposit.as_view(), name="bank_deposit"),

]