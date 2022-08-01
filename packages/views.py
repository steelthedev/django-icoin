from django.shortcuts import render
from .models import Packages
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import HttpResponse, response
from .serializers import PackageSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.contrib.auth.models import User
from rest_framework import status, authentication, permissions
import csv

@api_view(['GET'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def GetPackages(request):
    if request.method == "GET":
        try:
            transaction = Packages.objects.all()
        except:
            return HttpResponse( status = 201 )
        serializer = PackageSerializer(transaction, many=True)
        return Response(serializer.data)


def createPackage(request):
    with open("packages/packages.csv") as file:
        package = csv.reader(file, delimiter=",")
        next(package)
        [Packages.objects.create(title=p[0], amount = p[1], roi = p[3], referral_bonus= p[4]) for p in package]
        return True