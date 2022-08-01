import uuid
import base64
from tasks.models import Task, TaskTable 
from distutils.command.upload import upload
from email.policy import default
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AbstractUser, UserManager
from django.db.models.signals import post_save
from django.db.models import Sum
from django.db.models import Q
from django.shortcuts import reverse
import client.models
import datetime
from django.conf import settings

class CustomUserManager(UserManager):
    def get_by_natural_key(self, username):
        return self.get(
            Q(**{self.model.USERNAME_FIELD: username}) |
            Q(**{self.model.EMAIL_FIELD: username})
        )


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, max_length=200)
    username = models.CharField(max_length=200, unique=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)


    USERNAME_FIELD = "username"
    EMAIL_FIELD ="email"

    REQUIRED_FIELDS = []

    objects = CustomUserManager()


class Profile(models.Model):

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, blank=True)
    type = models.CharField(max_length=100, default="user", blank=True)
    image = models.ImageField(blank=True, upload_to="user/", null=True, default="user/default/default.png")
    email = models.EmailField(max_length=150, blank=True)
    username = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=100, blank=True)
    referral_code = models.UUIDField(editable=True, default = uuid.uuid4, primary_key=False)



    def __str__(self):
        return self.user.username


    def get_profile_picture(self):
        if self.image:
            return settings.WEBSITE_URL + self.image.url

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance= None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
        client.models.Wallet.objects.create(user=instance, profile=instance.profile)
        tasks = TaskTable.objects.all()[:1]
        if tasks:
            title_name = "Day-{}"
            [Task.objects.create(user=instance, image=task.image, title =title_name.format(datetime.date.today()) )for task in tasks]
