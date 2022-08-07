
from decimal import Decimal
from random import randint
from unicodedata import decimal
import requests
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import HttpResponse, response
from .serializers import TransactionSerializer, WalletSerializer, BankSerializer
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import authentication_classes, permission_classes
from .models import Transaction, Wallet, Bank
from rest_framework import status, authentication, permissions
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail  
from django.dispatch import receiver
from django.urls import reverse
from django.conf import settings

# Create your views here.


@api_view(["GET"])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def getTransaction(request):
    if request.method == "GET":
        profile = request.user.profile
        try:
            transaction = Transaction.objects.filter(profile=profile)
        except:
            return HttpResponse( status = 201 )
        serializer = TransactionSerializer(transaction, many=True)
        return Response(serializer.data)

@api_view(["GET"])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def getPendingTransaction(request):
    if request.method == "GET":
        try:
            transaction = Transaction.objects.filter(status=Transaction.PENDING)
        except:
            return HttpResponse( status = 201 )
        serializer = TransactionSerializer(transaction, many=True)
        return Response(serializer.data)

@api_view(["POST"])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def DisapproveTransaction(request,id):
    if request.user.is_staff:
        if request.method == "POST":
            profile = request.user.profile
            if profile.type == "admin":
                try:
                    transaction = Transaction.objects.get(pk=id)
                    transaction.status = Transaction.FAILED
                    transaction.save()
                    return HttpResponse(status=200)
                except:
                    return HttpResponse( status = 201 )
            else:
                return HttpResponse(status=201)
      
@api_view(["POST"])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def ApproveTransaction(request,id):
    if request.user.is_staff:
        if request.method == "POST":
            profile = request.user.profile
            if profile.type == "admin":
                try:
                    transaction = Transaction.objects.get(pk=id)
                    try:
                        if transaction.type == Transaction.WITHDRAWAL:
                            wallet = Wallet.objects.get(profile=transaction.profile)
                            withdrawable = int(wallet.wallet_balance + wallet.investment_balance) - int(0.08 * (wallet.wallet_balance + wallet.investment_balance)) 

                            if not withdrawable < transaction.amount:
                                try:
                                    if transaction.mode == Transaction.BANK: 
                                        wallet_b = wallet.wallet_balance - transaction.amount
                                        if wallet_b > 0:
                                            wallet.wallet_balance = wallet_b
                                        elif wallet_b <= 0:
                                              wallet.wallet_balance = 0
                                    elif transaction.mode == Transaction.USDT:
                                        wallet_b = int(wallet.wallet_balance - (float(transaction.amount) / 0.001795))
                                        print(wallet_b)
                                        if wallet_b > 0:
                                            wallet.wallet_balance = wallet_b
                                        elif wallet_b <= 0:
                                            wallet.wallet_balance = 0
                                except:
                                    return HttpResponse(status =401)
                                wallet.investment_balance = 0
                                wallet.Active_investment = None
                                wallet.save()
                            else:
                                transaction.delete()
                        elif transaction.type == Transaction.DEPOSIT:
                            
                            wallet = Wallet.objects.get(profile=transaction.profile)
                            wallet_b = round(float(transaction.amount) / 0.001795)
                            wallet.wallet_balance += wallet_b 
                            wallet.save()
                    except:
                        return Response(status=401)
                    transaction.status = Transaction.SUCCESS
                    transaction.save()
                    return Response(status=200)
                except:
                    return Response( status = 401 )
            else:
                return HttpResponse(status=201)
        

@api_view(["GET"])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def GetWallet(request):
    if request.method == "GET":
        profile = request.user.profile
        try:
            wallet = Wallet.objects.get(profile=profile, user = request.user)
        except:
            return HttpResponse(status=404)
        serializer = WalletSerializer(wallet, many=False)
        return Response(serializer.data)


@api_view(["POST",])
def verifyClient(request):

  account_number = request.data.get('account_number','')
  bank_code = request.data.get('bank','')
  
  base_url = 'https://api.paystack.co'
  path = f"/bank/resolve?account_number={account_number}&bank_code={bank_code}"
  PAYSTACK_SECRET_KEY = "sk_test_99b8fd6afab2ec0caae8c76063c25d94f5a8096e"

  headers = {
      "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}" ,
      "Content-Type":'application/json',
  }

  url = base_url + path
  
  response = requests.get(url, headers = headers)
  
  if response.status_code == 200:
      response_data = response.json()
      return Response(response_data)
  else:
      print(account_number)

@api_view(["GET","POST"])
def MakeTransfer(request):
     
  base_url = 'https://api.paystack.co'
  path = f"/transferrecipient"
  PAYSTACK_SECRET_KEY = "sk_test_b1630e59eb70f2592023210935c7894455b9ac1b"

  headers = {
      "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}" ,
      "Content-Type":'application/json',
  }
  params={
    "type":"nuban",
    "name": "Akinwumi Iyanuoluwa Ayomiposi",
    "account_number": "3033701410", 
    "bank_code": "011", 
    }
  url = base_url + path

  response = requests.post(url, headers= headers, params=params)
  print(response.json())
  return Response(response.json())


@api_view(["POST",])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def UpdateWallet(request):
    if request.method == "POST":
        profile = request.user.profile
        
        try:
            account_number = request.data.get("account_number", '')
            account_name = request.data.get("account_name", '')
            wallet_address = request.data.get("wallet_address", '')
            password = request.data.get("password", '')
            bank = request.data.get("bank")

        except:
            return HttpResponse(status=201)
        data = {}
        if check_password(password, request.user.password):
           
            try:
                wallet = Wallet.objects.get(profile = profile)
            except:
                return HttpResponse(status = 404)
            wallet.wallet_address = wallet_address
            wallet.account_name = account_name
            wallet.account_number = account_number
            wallet.bank = Bank.objects.get(bank_code = bank)
            wallet.save()
            data["message"] = "Wallet updated successfully"
            return Response(data)
        else:
            return HttpResponse(status=201)
        



@api_view(["POST",])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def UpdateBalance(request):
    if request.user.is_authenticated:
        profile = request.user.profile
        if request.method == "POST":
            try:
                wallet = Wallet.objects.get(profile=profile)
            except:
                return HttpResponse(status = 201)

            paid = int(request.data.get("amount",''))
            reference = request.data.get("reference",'')
            if paid:
                wallet.wallet_balance += paid
                wallet.save()
                Transaction.objects.create(profile=profile, wallet=wallet, amount=paid, transaction_id=reference, type=Transaction.DEPOSIT, status=Transaction.SUCCESS)
                return HttpResponse(status=200)



@api_view(["POST",])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def RequestWithdrawal(request):
    if request.method == "POST":
        user = request.user
        profile = user.profile
        account_name = request.data.get("account_name",'')
        account_number = request.data.get("account_number",'')
        bank_name = request.data.get("bank_name",'')
        amount = request.data.get("amount",'')
        c_amount = request.data.get("c_amount",'')
        password = request.data.get("password",'')
        ref = request.data.get('ref',"")
        try:
            wallet = Wallet.objects.get(profile=profile, user=user)
        except:
            return HttpResponse(status = 404)
        if password:
            data ={}
            if wallet.investment_progress >= 100:
                if check_password(password, user.password):
                    
                    if bank_name and account_name and account_number and amount:
                        withdrawable = wallet.wallet_balance + wallet.investment_balance
                        if amount <= withdrawable:
                            try:
                                Transaction.objects.create(profile=profile,wallet=wallet, amount=amount, mode=Transaction.BANK, transaction_id=ref, type=Transaction.WITHDRAWAL, status=Transaction.PENDING)
                                data["message"] = "Withdrawal placed succesfully"
                                return Response(data)
                            except:
                                return HttpResponse(status=201)
                            return HttpResponse(status=200)           
                        else:
                            data["message"] = "Withdraw must be lesser than wallet balance"
                            return Response(data)    
                    elif c_amount:
                        withdrawable = "{:.2f}".format((wallet.wallet_balance + wallet.investment_balance) * 0.001795)
                        
                        if c_amount <= withdrawable:
                            coin_ref = "usdt-{}".format(randint(0,20000))
                            Transaction.objects.create(profile=profile, amount=c_amount,wallet=wallet, transaction_id=coin_ref, mode=Transaction.USDT, type=Transaction.WITHDRAWAL, status=Transaction.PENDING)
                            data["message"] = "Withdrawal placed succesfully"
                            return Response(data)
                        return HttpResponse(status=401)
                else:
                    data["message"] = "Incorrect Password"
                    return Response(data)
            else:
                data["message"] = "You cant withdraw now, fulfill all tasks for five days"
                return Response(data)
@api_view(["GET"])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def GetBank(request):
    if request.method == "GET":
        profile = request.user.profile
        try:
            bank = Bank.objects.all()
        except:
            return HttpResponse(status=404)
        serializer = BankSerializer(bank, many=True)
        return Response(serializer.data)
