from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from .models import Profile, CustomUser

admin.site.register(Profile)
admin.site.register(CustomUser, UserAdmin)