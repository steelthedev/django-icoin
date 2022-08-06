
from django.db import models
import string
import random
from django.utils.text import slugify
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms import MultipleChoiceField
# Create your models here.


def rand_slug():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))



class Task(models.Model):
    user = models.ForeignKey("accounts.CustomUser",on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200,null=True, blank=True)
    image = models.FileField(null=True, blank=True)
    active = models.BooleanField(default=True, null=True)
    task_screenshot = models.FileField(null=True, blank=True)
    created_on = models.DateField(auto_now_add=True, null=True)


    def __str__(self):
        return self.user.first_name

    def get_task_picture(self):
        if self.image:
            return settings.WEBSITE_URL + self.image.url

   

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def update_task_signal(sender, instance, created, **kwargs):
    if created:
        title_name = "Day-{}"
       
        
   





class TaskTable(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    image = models.FileField(null=True, blank=True)
    active = models.BooleanField(default=True,null=True, blank=True)
    created_on = models.DateField(auto_now_add=True,null=True, blank=True)

    def __str__(self) -> str:
        return self.image.url