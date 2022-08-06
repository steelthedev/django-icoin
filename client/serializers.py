

from .models import Bank, Transaction,Wallet
from rest_framework import serializers
from packages.serializers import PackageSerializer
from accounts.serializers import ProfileSerializer


class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = '__all__'


class WalletSerializer(serializers.ModelSerializer):
    Active_investment = PackageSerializer(many=False)
    bank = BankSerializer(many=False)
    class Meta:
        model = Wallet
        fields = ('id','wallet_balance', 'referral_balance', 'referral_count','Active_investment','investment_progress','investment_balance','wallet_address','account_name','account_number','bank')

class TransactionSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many=False)
    wallet = WalletSerializer(many=False)
    class Meta:
        model = Transaction
        fields = ('id','transaction_id', 'transaction_date', 'status','type','amount','get_transaction_picture','mode','image','wallet', 'profile')




