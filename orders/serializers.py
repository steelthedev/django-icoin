import email
from logging import raiseExceptions
from django.http import Http404, HttpRequest, HttpResponse
from requests import Response
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *
from client.models import Wallet, Referral
from packages.serializers import PackageSerializer
from rest_framework.fields import CurrentUserDefault

class MyOrderItemSerializer(serializers.ModelSerializer):    
    package = PackageSerializer()

    class Meta:
        model = OrderItem
        fields = (
            "price",
            "package",
        )

class MyOrderSerializer(serializers.ModelSerializer):
    items = MyOrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "full_name",
            "email",
            "phone",
            "items",
            "paid_amount"
        )

class OrderItemSerializer(serializers.ModelSerializer):    
    class Meta:
        model = OrderItem
        fields = (
            "price",
            "package",
        )

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "full_name",
            "email",
            "phone",
            "paid_amount",
            "items"
            
        )
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        user_wallet = Wallet.objects.get(user = self.context["request"].user)
        if not user_wallet.Active_investment and user_wallet.wallet_balance >= self.validated_data["paid_amount"]:
            order = Order.objects.create(**validated_data)
            wallet = Wallet.objects.get(profile=order.user.profile)
            order_item = [OrderItem.objects.create(order=order, **item_data) for item_data in items_data if wallet.wallet_balance >= order.paid_amount and not wallet.Active_investment]
            
            if order_item:

                if wallet.wallet_balance >= order.paid_amount and not wallet.Active_investment:
                    wallet.investment_balance = order.paid_amount
                    wallet_b = wallet.wallet_balance - order.paid_amount
                    if wallet_b <= 0:
                        wallet.wallet_balance = 0
                    wallet.wallet_balance = wallet_b
                    wallet.investment_progress = 0
                    wallet.Active_investment= OrderItem.objects.get(order = order).package
                    wallet.save()
                    try:
                        referral = Referral.objects.get(referred = order.user.profile)
                        if referral:
                            refree_wallet = Wallet.objects.get(profile = referral.profile)
                            refree_wallet.wallet_balance += OrderItem.objects.get(order = order).package.referral_bonus
                            refree_wallet.referral_balance += OrderItem.objects.get(order = order).package.referral_bonus
                            refree_wallet.save()
                    except:
                        pass
                
            return order
        return Http404 
   
