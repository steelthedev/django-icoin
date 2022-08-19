
import profile
from random import randint
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import HttpResponse
from .serializers import *
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.contrib.auth.hashers import check_password
from rest_framework import status, authentication, permissions
from accounts.models import Profile
from django.conf import settings
from client.models import Transaction
from rest_framework.views import APIView
# Create your views here.
@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def checkout(request):
    password = request.data.get("password", '')
    if password:
        if check_password(password, request.user.password):
            serializer = OrderSerializer(context={"request":request},data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(user = request.user)
                return HttpResponse(status=200)
            return HttpResponse(status=400)
        return HttpResponse(status = 401)
    return HttpResponse(status = 400)

@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def CoinDeposit(request):
    if request.method == "POST":
        profile = request.user.profile
        image = request.data.get("image")
        amount = request.data.get("amount",'')
        data = {}
        if image:
            c_ref = "usdt-{}".format(randint(0,20000))
            Transaction.objects.create(profile=profile, mode=Transaction.USDT, amount=amount, transaction_id=c_ref, type=Transaction.DEPOSIT, status=Transaction.PENDING)
            data["message"] = "Deposit request made, be patient as it takes longer time to approve deposits through usdt"
            return Response(data)
        
        return HttpResponse(status=402)
    return Http404


class coinDeposit(APIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes =[permissions.IsAuthenticated]
    

    def post(self,request):
        if request.method == "POST":
            image = request.data.get("image")
            amount = request.data.get("amount",'')
            data = {}
            if image:
                profile =request.user.profile
                wallet = Wallet.objects.get(profile =profile)
                c_ref = "usdt-{}".format(randint(0,20000))
                Transaction.objects.create(profile=profile, wallet=wallet, image=image, amount=amount,mode=Transaction.USDT, transaction_id=c_ref, type=Transaction.DEPOSIT, status=Transaction.PENDING)
                data["message"] = "Deposit request made, be patient as it takes longer time to approve deposits through usdt"
                return HttpResponse(status=200)
            return HttpResponse(status = 401)




class bankDeposit(APIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes =[permissions.IsAuthenticated]
    

    def post(self,request):
        if request.method == "POST":
            image = request.data.get("image")
            amount = request.data.get("amount",'')
            data = {}
            if image:
                profile =request.user.profile
                wallet = Wallet.objects.get(profile =profile)
                d_ref = "bank-{}".format(randint(0,20000))
                Transaction.objects.create(profile=profile, wallet=wallet, image=image, amount=amount,mode=Transaction.BANK, transaction_id=d_ref, type=Transaction.DEPOSIT, status=Transaction.PENDING)
                data["message"] = "Deposit request made, be patient as it takes longer time to approve deposits through usdt"
                return HttpResponse(status=200)
            return HttpResponse(status = 401)