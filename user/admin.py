from django.contrib import admin
from .models import UserOTP
from .models import CustomUser
# Register your models here.

admin.site.register(UserOTP)
admin.site.register(CustomUser)