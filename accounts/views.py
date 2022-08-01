
from django.conf import settings
from django.shortcuts import render
from requests import request
from client.models import Referral, Wallet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import HttpResponse, response
from .serializers import ProfileSerializer, RegisterSerializer
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import authentication_classes, permission_classes
from .models import Profile
from rest_framework import status, authentication, permissions
from django.contrib.auth.hashers import make_password, check_password
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail
from django.dispatch import receiver
from django.urls import reverse
from django.conf import settings


@api_view(["POST",])
def RegisterView(request):
    if request.method == "POST":
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            account = serializer.save()
            account.refresh_from_db()
            account.profile.username = account.username
            account.profile.full_name = account.first_name
            account.profile.email = account.email
            account.profile.phone = request.data.get("phone",'')
            referral_code =  request.data.get("referral_code",'')
            if referral_code:
                refree = Profile.objects.get(referral_code = referral_code)
                Referral.objects.create(profile=refree, referred = account.profile)
                refree_wallet = Wallet.objects.get(profile = refree)
                refree_wallet.referral_count += 1
                refree_wallet.save() 
            account.save()
        else:
            return HttpResponse( status = 201 )
        return HttpResponse( status = 200 )


@authentication_classes([])
class SFObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        return super(SFObtainAuthToken, self).post(request, *args, **kwargs)


@api_view(["GET","PUT"])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def ProfileView(request):
    if request.method == "GET":
        try:
            profile = Profile.objects.get(user = request.user)
        except:
            return HttpResponse( status = 201 )
        serializer = ProfileSerializer(profile, many = False)
        return Response(serializer.data)


@api_view(["PUT","PATCH"])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def ProfileEdit(request):
    if request.method == "PATCH":
        try:
            profile = Profile.objects.get(user = request.user)
        except:
            return HttpResponse( status = 201 )
        serializer = ProfileSerializer(profile, data = request.data)
        if serializer.is_valid():
            old_password = request.data.get("old_password",'')
            new_password = request.data.get("new_password",'')
            if old_password and new_password:
                data={}
                user = request.user
                if check_password(old_password,user.password):
                    user.password = make_password(new_password)
                    user.save()
                    data["message"] = "Password saved successfully"
                elif not check_password(user.password,old_password):
                    data["error"] = "Old password is incorrect"
                    return Response(data)
            serializer.save()
            return HttpResponse(status = 200)
        return Response(serializer.data)

@api_view(["PUT","PATCH"])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def ProfilePictureEdit(request):
    if request.method == "PATCH":
        image = request.data.get("image")
        try:
            profile = Profile.objects.get(user = request.user)
        except:
            return HttpResponse( status = 201 )
        profile.image = image
        profile.save()
        return HttpResponse(status = 200)
        


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    data ={}
    email_plaintext_message = "Dear {} \n\n {}?token={}".format( reset_password_token.user.username, reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {user}".format(user="user"),
        # message:
        email_plaintext_message,
        # from:
        settings.EMAIL_HOST_USER,
        # to:
        [reset_password_token.user.email],

        fail_silently=False

    )
   
