from django.db import models
from packages.models import Packages
from accounts.models import CustomUser

# Create your models here.
   
class Order(models.Model):
    user = models.ForeignKey(CustomUser, related_name='orders', on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, blank=True)
    email = models.CharField(max_length=100,blank=True)
    phone = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_amount = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
   

    class Meta:
        ordering = ['-created_at',]
    
    def __str__(self):
        return self.full_name

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    package = models.ForeignKey(Packages, related_name='items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return '%s' % self.id