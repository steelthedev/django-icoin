from . import views
from django.urls import path,include
urlpatterns = [
    path('', views.GetTask),
    path('create_task', views.createTask),
    path('update_task', views.UpdateTask),
    path('create_task_table', views.NewTask),
    path('set_inactive/<int:id>', views.SetTask)
   
]
