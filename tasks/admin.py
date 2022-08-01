from django.contrib import admin
from .models import Task,TaskTable
# Register your models here.

admin.site.register(Task)
admin.site.register(TaskTable)