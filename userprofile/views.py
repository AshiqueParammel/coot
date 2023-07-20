from django.shortcuts import render,redirect
from django.views.decorators.cache import cache_control,never_cache

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate,login,logout

from django.contrib.auth.models import User
from django.contrib import messages,auth
from django.contrib.auth.password_validation import validate_password

# verification email
import re
import random
from django.conf import settings
import random
from django.core.mail import send_mail
from django.core.validators import validate_email
# Create your views here.

@login_required(login_url='user_login1')
def userprofile(request):
   
    return render(request,'userprofile/userprofile.html')