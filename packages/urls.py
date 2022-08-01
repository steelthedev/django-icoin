from django.urls import path
from . import views

urlpatterns = [
    path('package-list', views.GetPackages, name="packages"),
    path('package-create', views.createPackage, name="create-package"),

]