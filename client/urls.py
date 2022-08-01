
from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('user/transaction', views.getTransaction),
    path('admin-user/transaction', views.getPendingTransaction),
    path('admin-user/transaction-decline/<int:id>', views.DisapproveTransaction),
    path('admin-user/transaction-approve/<int:id>', views.ApproveTransaction),
    path('user/wallet', views.GetWallet),
    path('user/wallet/verify-account', views.verifyClient),
    path('user/wallet/update', views.UpdateWallet),
    path('user/wallet/update-amount', views.UpdateBalance),
    path('user/wallet/withdraw', views.RequestWithdrawal),
    path('user/wallet/bank-list', views.GetBank),
    path('maketransfer', views.MakeTransfer)
]
