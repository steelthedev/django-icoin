
from django.conf import settings
from packages.models import Packages
from django.db import models
from accounts.models import Profile,CustomUser

# Create your models here.
import uuid
import base64

class Transaction(models.Model):

    WITHDRAWAL ='withdrawal'
    DEPOSIT = 'deposit'
    
    SUCCESS = 'success'
    FAILED = 'failed'
    PENDING = 'pending'

    USDT = "usdt"
    BANK = "bank"


    TYPE_CHOICES =[
        (WITHDRAWAL, 'Withdrawal'),
        (DEPOSIT, 'Deposit'),
        
    ]


    STATUS_CHOICES =[
        (SUCCESS, 'Success'),
        (FAILED, 'Failed'),
        (PENDING,'Pending')
    ]

    PAYMENT_MODE =[
        (USDT, 'Usdt'),
        (BANK, 'Bank'),
    ]


    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, related_name="profile", null=True)
    type = models.CharField(max_length=200, choices=TYPE_CHOICES)
    amount = models.DecimalField(max_digits=30, decimal_places=3)
    transaction_date = models.DateTimeField(auto_now_add=True)
    transaction_id =  models.CharField(max_length=400)
    status = models.CharField(max_length=200, choices=STATUS_CHOICES, default=PENDING)
    mode = models.CharField(max_length=200, choices=PAYMENT_MODE)
    image = models.ImageField(null=True, blank=True)
    wallet = models.ForeignKey("Wallet" ,null=True, on_delete=models.SET_NULL)


    def __str__(self) -> str:
        return f" {self.profile} - {self.transaction_date}"

    def get_transaction_picture(self):
        if self.image:
            return settings.LOCAL_URL + self.image.url

class Bank(models.Model):
    bank_name = models.CharField(max_length=500)
    bank_code = models.CharField(max_length=500)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.bank_name


class Wallet(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name="user")
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name="wallet_profile")
    wallet_balance = models.IntegerField(default=0.00, null=True, blank=True)
    wallet_address = models.CharField(max_length=500, null=True,blank=True)
    account_number = models.CharField(max_length=500, null=True,blank=True)
    account_name = models.CharField(max_length=500, null=True, blank=True)
    referral_balance = models.IntegerField(default=0.00,blank=True,null=True)
    investment_balance = models.IntegerField(default=0.00, null=True, blank=True)
    referral_count = models.IntegerField(null=True, default=0, blank=True)
    investment_progress = models.IntegerField(null=True, default=0,blank=True)
    Active_investment = models.ForeignKey(Packages, blank=True,on_delete=models.SET_NULL, null=True, related_name="active_investment" )
    bank = models.ForeignKey(Bank, on_delete=models.SET_NULL, null=True, blank=True)
    

    def __str__(self) -> str:
        return self.user.profile.full_name


class Referral(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, related_name="referral_profile", null=True)
    referred = models.ForeignKey(Profile, on_delete=models.SET_NULL, related_name="referred_profile", null=True)
   
    created_on = models.DateTimeField(auto_now_add=True)


    def __str__(self) -> str:
        return self.profile.full_name



