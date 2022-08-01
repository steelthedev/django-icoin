
from rest_framework import serializers
from .models import Task,TaskTable



class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id','title','created_on','active','get_task_picture','user')




class TaskTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskTable
        fields = '__all__'