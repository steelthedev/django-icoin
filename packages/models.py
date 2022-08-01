from django.db import models
from accounts.models import Profile
# Create your models here.
class Packages(models.Model):
    title = models.CharField(max_length=200, null=True)
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    amount = models.IntegerField(null=True)
    roi = models.IntegerField(null=True)
    referral_bonus = models.IntegerField(null=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title