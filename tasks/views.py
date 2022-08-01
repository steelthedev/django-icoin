
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import HttpResponse, response
from .serializers import TaskSerializer,TaskTableSerializer
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import authentication_classes, permission_classes
from .models import Task,TaskTable
from rest_framework import status, authentication, permissions
from accounts.models import CustomUser
from client.models import Wallet
import datetime



def Calc_Returns(roi):
    returns_per_day = (5/100) * roi
    return returns_per_day


@api_view(["GET"])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def GetTask(request):
    user = request.user
    try:
        task = Task.objects.filter(user=user, active = True)
    except:
        return HttpResponse( status = 201 )
    serializer = TaskSerializer(task, many=True)
    
    return Response(serializer.data)
        

@api_view(["GET","POST"])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def SetTask(request,id):
    user = request.user
    profile = request.user.profile
    data ={}
    if request.method == "POST":
        task_image = request.data.get("image")
        try:
            wallet = Wallet.objects.get(profile = profile)
            task = Task.objects.get(user=user, pk=id)
            active_investment = wallet.Active_investment
            try:
                if not active_investment:
                    return HttpResponse(status=201)
                elif active_investment:
                    try:
                        task.task_screenshot = task_image
                    except:
                        return HttpResponse(status = 404)
                    task.active = False
                    wallet.investment_balance += Calc_Returns(active_investment.amount)
                    wallet.investment_progress += 20
                    wallet.save()
                    task.save()
            except:
                return HttpResponse(status=201)
            
            data ={
                "success":"Success"
            }
        except:
            return HttpResponse( status = 201 )
        
        return Response(data["success"])


@api_view(["GET","POST"])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def NewTask(request):
    if request.method == "POST":
        serializer = TaskTableSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=201)

def createTask(request):
    users = CustomUser.objects.all()
    try:
        for user in users:
            Task.objects.filter(user=user).delete()
            Task.objects.create(user=user, title="task 6")
    except:
        pass

@api_view(["POST"])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def UpdateTask(request):
    if request.method == "POST":
        data = {}
    
        users=CustomUser.objects.all()

        if TaskTable.objects.all().count() > 1:
            TaskTable.objects.filter(id__in=list(TaskTable.objects.values_list('pk', flat=True)[:1])).delete()
        task_update = TaskTable.objects.all()[:1]
        if task_update:
            try:
               
                title = "Daily Task - {}"
                Task.objects.all().delete()
                [Task.objects.create(image=task.image, user=user, title=title.format(datetime.date.today())) for task in task_update for user in users ]
                data["message"] = "Success"
                return Response(data)
            except:
                return HttpResponse(status=201)
        else:
                return HttpResponse(status=202)