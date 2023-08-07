from django.db import models
from user.models import CustomUser
from variant.models import Variant

# Create your models here.

class Wishlist(models.Model):
    user = models.ForeignKey(CustomUser,  on_delete=models.CASCADE)
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE) 
    created_at = models.DateTimeField(auto_now_add=True)

