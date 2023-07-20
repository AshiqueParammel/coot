from django.shortcuts import render,redirect
from django.views.decorators.cache import cache_control,never_cache

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate,login,logout

from django.contrib.auth.models import User
from django.contrib import messages,auth
from django.contrib.auth.password_validation import validate_password

# verification email
from .models import UserOTP,CustomUser
import re
import random
from django.conf import settings
import random
from django.core.mail import send_mail
from django.core.validators import validate_email
# Create your views here.

def user_signup(request):
    
    if request.method == 'POST':
        
        get_otp=request.POST.get('otp')
        if get_otp:
            get_email=request.POST.get('email')
            user=CustomUser.objects.get(email=get_email)

            if int(get_otp)==UserOTP.objects.filter(user=user).last().otp:
                user.is_active=True
                user.save()
                auth.login(request,user)
                # messages.success(request,f'Account is created for {user.email}')
                UserOTP.objects.filter(user=user).delete()
                return redirect('home')
            else:
                messages.warning(request,f'you Entered a Wrong OTP')
                return render(request,'user\signup.html',{'otp':True,'user':user})
        else:
            get_otp=request.POST.get('otp1')
            email=request.POST.get('user1')
            if get_otp:
                user=CustomUser.objects.get(email=email)
                messages.error(request,'field cannot empty!')
                return render(request,'user\signup.html',{'otp':True,'user':user})
            else:
                firstname=request.POST['fname']
                lastname=request.POST['lname']
                phonenumber=request.POST['phonenumber']
                email=request.POST['email']
                password1=request.POST['password1']
                password2=request.POST['password2']
                
                context={
                        'pre_firstname' :firstname,
                        'pre_lastname':lastname,
                        'pre_phonenumber':phonenumber,
                        'pre_email':email,
                        'pre_password1':password1,
                        'pre_password2':password2
                }
                
                if phonenumber.strip()=='' or password1.strip()==''or password2.strip()==''  or email.strip()=='' or firstname.strip()=='' or lastname.strip()=='' :
                    messages.error(request,'field cannot empty!')
                    return render(request,'user\signup.html',context )
                
                elif CustomUser.objects.filter(phone_number=phonenumber).exists():
                    user = CustomUser.objects.get(phone_number=phonenumber)
                    if user.last_login is None:
                            user.delete()
                    else:
                        messages.error(request,'phonenumber alredy exist!')
                        context['pre_phonenumber']=''
                        return render(request,'user\signup.html',context )
                
                elif not re.search(re.compile(r'(\+91)?(-)?\s*?(91)?\s*?(\d{3})-?\s*?(\d{3})-?\s*?(\d{4})'), phonenumber):   
                    messages.error(request,'phonenumber should only contain numeric!')  
                    context['pre_phonenumber']=''
                    return render(request,'user\signup.html',context )
                    
                elif CustomUser.objects.filter(email=email).exists():
                    user = CustomUser.objects.get(email=email)
                    if user.last_login is None:
                            user.delete()
                    else:        
                        messages.error(request,'email already exist!')
                        context['pre_email']=''
                        return render(request,'user\signup.html',context ) 
                    
                elif password1 != password2:
                    messages.error(request,"password doesn't match")
                    context['pre_password1']=''
                    context['pre_password2']='' 
                    return render(request,'user\signup.html',context )
                
                
                email_check=validateemail(email)
                if email_check is False:
                    messages.error(request,'email not valid!')
                    context['pre_email']=''
                    return render(request,'user\signup.html',context )
                
                
                password_check=validatepassword(password1)
                if password_check is False:
                    messages.error(request,'Enter strong password!')
                    context['pre_password1']=''
                    context['pre_password2']=''
                    return render(request,'user\signup.html',context)
                
                phonenumber_checking=len(phonenumber)
                if not  phonenumber_checking==10:
                    messages.error(request,'phonenumber should be must contain 10digits!')  
                    context['pre_phonenumber']=''
                    return render(request,'user\signup.html',context )
                if phonenumber=='0000000000':
                    messages.error(request,'phonenumber not valid!')  
                    context['pre_phonenumber']=''
                    return render(request,'user\signup.html',context )
                    
                    
                    
                user=CustomUser.objects.create_user(first_name=firstname,last_name=lastname,username=phonenumber,phone_number=phonenumber,email=email,password=password1)
                user.is_active=False
                user.last_login=None
                user.save()
                user_otp=random.randint(100000,999999)
                UserOTP.objects.create(user=user,otp=user_otp)
                mess=f'Hello \t{user.first_name},\nYour OTP to verify your account for Coot is {user_otp}\n Thanks You!'
                send_mail(
                    "Welcome to Coot , verify your Email",
                    mess,
                    settings.EMAIL_HOST_USER,
                    [user.email],

                    fail_silently=False
                    )
                return render(request,'user\signup.html',{'otp':True,'user':user})  
        
    return render(request,'user\signup.html')
        
        
def validateemail(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False
    
def validatepassword(password1):
    try:
        validate_password(password1)
        return True
    except  ValidationError:
        return  False
            

    
def user_login1(request):
    if request.user.is_authenticated:
        return redirect('userprofile')#dashboard user
   
    if request.method=='POST':
        number_mail=request.POST['number_mail']
        password=request.POST['password']
        
        if number_mail.strip()=='' or password.strip()=='':
            messages.error(request,'field cannot empty!')
            return redirect('user_login1')
        
        if CustomUser.objects.filter(phone_number=number_mail):
            user=CustomUser.objects.get(phone_number=number_mail)
            username=user.username
        else:
            if CustomUser.objects.filter(email=number_mail):
                user=CustomUser.objects.get(email=number_mail)
                username=user.username
            else:
                messages.error(request,'Enter valid email or phone numebr!')
                return redirect('user_login1')
                             
        user=authenticate(username=username,password=password)
        
        if user is not None:
            
            if user.is_active:
                login(request,user)
                return redirect('home') 
            else:
                messages.warning(request,'your account has been blocked!')
                return redirect('user_login1')
            
        else:
            messages.error(request,'invalid username or password!')
            return redirect('user_login1')
    
    return render(request,'user\login.html')
  
def user_loginotp(request):
   
    if request.method=='POST':
        get_otp=request.POST.get('otp')
        if get_otp:
            get_email=request.POST.get('email')
            user=CustomUser.objects.get(email=get_email)
            if int(get_otp)==UserOTP.objects.filter(user=user).last().otp:
                auth.login(request,user)
                UserOTP.objects.filter(user=user).delete()
                return redirect('home')   
            else:
                messages.warning(request,'You Entered a wrong OTP!')
                return render(request,'user\loginwithotp.html',{'otp':True,'user':user})  
        else:
            get_otp=request.POST.get('otp1')
            email=request.POST.get('user1')
            if get_otp:
                user=CustomUser.objects.get(email=email)
                messages.error(request,'field cannot empty!')
                return render(request,'user\loginwithotp.html',{'otp':True,'user':user})
            else:
                email=request.POST['email']
            
                if email.strip()=='':
                    messages.error(request,'field cannot empty!')
                    return redirect('user_loginotp')
            
        
                email_check=validateemail(email)
                if email_check is False:
                    messages.error(request,'email not valid!')
                    return render(request,'user\loginwithotp.html')
                        
                if CustomUser.objects.filter(email=email):
                    user=CustomUser.objects.get(email=email)
                    user_otp=random.randint(100000,999999)
                    UserOTP.objects.create(user=user,otp=user_otp)
                    message=f'Hello\t{user.first_name},\n Your OTP to verify your account for Coot is {user_otp}\n Thanks' 
                    send_mail(
                        "welcome to Coot Verify Email",
                        message,
                        settings.EMAIL_HOST_USER,
                        [user.email],
                        fail_silently=False
                    )
                    return render (request,'user\loginwithotp.html',{'otp':True,'user':user}) 
                else:
                    messages.error(request,'email does not exist!')
                    return render(request,'user\loginwithotp.html')
    return render (request,'user\loginwithotp.html')  

@login_required(login_url='user_login1')
def logout1(request):
    logout(request)
    return redirect('home')

def forgot_password(request):
    if request.method=='POST':
        get_otp=request.POST.get('otp')
        
        if get_otp:
            get_email=request.POST.get('email')
            user=CustomUser.objects.get(email=get_email)
            if int(get_otp)==UserOTP.objects.filter(user=user).last().otp:
                password1 = request.POST.get('password1')
                password2 = request.POST.get('password2')
                context ={
                                'pre_otp':get_otp,
                            }
                if password1.strip()==''or password2.strip()=='':
                    messages.error(request,'field cannot empty !')
                    return render(request,'user\password_forgot.html',{'otp':True,'user':user,'pre_otp':get_otp})
                
                elif password1 != password2:
                    messages.error(request,'Password does not match!')
                    return render(request,'user\password_forgot.html',{'otp':True,'user':user,'pre_otp':get_otp})
                    
                Pass = validatepassword(password1)
                if Pass is False:
                    messages.error(request,'Please enter Strong password!')
                    return render(request,'user\password_forgot.html',{'otp':True,'user':user,'pre_otp':get_otp})
                user.set_password(password1)
                user.save()
                UserOTP.objects.filter(user=user).delete()
                messages.success(request,'Your password is changed!')
                return redirect('user_login1')
            else:
                messages.warning(request,'You Entered a wrong OTP!')
                return render(request,'user\password_forgot.html',{'otp':True,'user':user})  
        else:
            
            get_otp=request.POST.get('otp1')
            email=request.POST.get('user1')
            if get_otp:
                user=CustomUser.objects.get(email=email)
                messages.error(request,'field cannot empty!')
                return render(request,'user\password_forgot.html',{'otp':True,'user':user})
                
            else:   
                email=request.POST['email']
                
                if email.strip()=='':
                    messages.error(request,'field cannot empty!')
                    return render(request,'user\password_forgot.html')
                
                email_check=validateemail(email)
                if email_check is False:
                    messages.error(request,'email not valid!')
                    return render(request,'user\password_forgot.html')
            
                if CustomUser.objects.filter(email=email):
                    user=CustomUser.objects.get(email=email)
                    user_otp=random.randint(100000,999999)
                    UserOTP.objects.create(user=user,otp=user_otp)
                    message=f'Hello\t{user.first_name},\n Your OTP to verify your account for Coot is {user_otp}\n Thanks' 
                    send_mail(
                        "welcome to Coot Verify Email",
                        message,
                        settings.EMAIL_HOST_USER,
                        [user.email],
                        fail_silently=False
                    )
                    return render (request,'user\password_forgot.html',{'otp':True,'user':user}) 
                else:
                    messages.error(request,'email does not exist!')
                    return render(request,'user\password_forgot.html')
    return render (request,'user\password_forgot.html')  

   
 