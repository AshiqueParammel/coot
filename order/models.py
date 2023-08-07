from django.db import models

# Create your models here.
from checkout.models import Order
from user.models import CustomUser
# Create your models here.

class Orderreturn(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    options = models.CharField(max_length=100,null=True)
    reason = models.TextField(null=True)
    
class Order_Cancelled(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    options = models.CharField(max_length=100,null=True)
    reason = models.TextField(null=True)    