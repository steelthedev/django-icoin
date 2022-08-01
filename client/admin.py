from django.contrib import admin
from .models import Transaction,Wallet,Referral,Bank
# Register your models here.


admin.site.register(Transaction)
admin.site.register(Wallet)
admin.site.register(Referral)
admin.site.register(Bank)