from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class UserOTP(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    timme_st = models.DateTimeField(auto_now=True)
    otp = models.IntegerField()

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return self.username
