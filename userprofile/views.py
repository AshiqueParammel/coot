import re
from django.forms import ValidationError
from django.shortcuts import render,redirect
from django.views.decorators.cache import cache_control,never_cache
from django.contrib.auth.decorators import login_required
from coot.settings import AUTH_USER_MODEL
from products.models import Product,Size,Color
from variant.models import Variant,VariantImage
from user.models import CustomUser
from .models import Address,Wallet
from checkout.models import Order,OrderItem
from django.contrib import messages
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
# Create your views here.

@login_required(login_url='user_login1')
def userprofile(request):
    
    # orders = Order.objects.filter(user=request.user).order_by('-created_at')
    # order_items = OrderItem.objects.filter(order__in=orders).order_by('-order__created_at')
    
    # for order in orders:
    #     all_orderitems_cancelled = all(order_item.status == 'Cancelled' for order_item in order.orderitem_set.all())

    #     if all_orderitems_cancelled:
    #         order.od_status = 'Cancelled'
    #     elif all(order_item.status == 'Delivered' for order_item in order.orderitem_set.all()):
    #         order.od_status = 'Delivered'
    #     elif all(order_item.status == 'Return' for order_item in order.orderitem_set.all()):
    #         order.od_status = 'Return'
    #     elif all(order_item.status == 'Processing' for order_item in order.orderitem_set.all()):
    #         order.od_status = 'Processing'
    #     else:
    #         order.od_status = 'Pending'

    #     order.save()
    
        # user_info = {
        # 'address': Address.objects.filter(user=request.user).first(),
        # 'user': User.objects.get(phone_number=request.user),
        # 'wallets': Wallet.objects.filter(user=request.user),
        # 'cart': Cart.objects.filter(user=request.user).order_by('-id'),
        # 'wishlist': Wishlist.objects.filter(user=request.user).order_by('-id'),
        # 'addresses': Address.objects.filter(user=request.user),
        # 'orders': orders,
        # 'order_items': order_items,
        #  }
        
        # return render(request,'userprofile/userprofile.html', user_info)
        return render(request,'userprofile/userprofile.html')



def checkout(request):
    
    return render(request,'userprofile/checkout.html')


def add_address(request):

    if request.method == 'POST':

        first_name=request.POST.get('firstname')
        last_name=request.POST.get('lastname')
        country=request.POST.get('country')
        address=request.POST.get('address')
        city=request.POST.get('city')
        pincode=request.POST.get('pincode')
        phone=request.POST.get('phone')
        email=request.POST.get('email')
        state=request.POST.get('state')
        order_note=request.POST.get('order_note')
        
        context={
            'pre_first_name': first_name,
            'pre_last_name':last_name,
            'pre_country':country,
            'pre_address':address,
            'pre_city':city,
            'pre_ pincode':pincode,
            'pre_phone':phone,
            'pre_email':email,
            'pre_state':state,
            'pre_order_note':order_note,
    
                }


        if request.user is None:
            return
        
        if first_name.strip() == '' : 
            messages.error(request,'names cannot be empty!!!')
            context['pre_first_name']=''
            return redirect('edit_address',context)
            
        if last_name.strip() == '':
            messages.error(request,'names cannot be empty!!!')
            context['pre_last_name']=''
            return redirect('edit_address',context)
        
        if country.strip()=='':
            messages.error(request,'Country cannot be empty')
            context['pre_country']=''
            return redirect('edit_address',context)
        if city.strip()=='':
            messages.error(request,'city cannot be empty')
            context['pre_city']=''
            return redirect('edit_address',context)
        if address.strip()=='':
            messages.error(request,'address cannot be empty')
            context['pre_address']=''
            return redirect('edit_address',context)
        if pincode.strip()=='':
            messages.error(request,'pincode cannot be empty')
            context['pre_ pincode']=''
            return redirect('edit_address',context)
        if not re.search(re.compile(r'^\d{6}$'),pincode ):  
            messages.error(request,'should only 6 contain numeric!')   
            context['pre_ pincode']=''
            return redirect('edit_address',context)
        if not re.search(re.compile(r'(\+91)?(-)?\s*?(91)?\s*?(\d{3})-?\s*?(\d{3})-?\s*?(\d{4})'),phone ): 
            messages.error(request,'Enter valid phonenumber!')
            context['pre_phone']=''
            return redirect('edit_address',context)
        if phone.strip()=='':
            messages.error(request,'phone cannot be empty')
            context['pre_phone']=''
            return redirect('edit_address',context)
        if email.strip()=='':
            messages.error(request,'email cannot be empty')
            context['pre_email']=''
            return redirect('edit_address',context)
        email_check=validateemail(email)
        if email_check is False:
            messages.error(request,'email not valid!')
            context['pre_email']=''
            return redirect('edit_address',context)
                   
        if state.strip()=='':
            messages.error(request,'state cannot be empty')
            context['pre_state']=''
            return redirect('edit_address',context)

        ads=Address()
        ads.user=request.user
        ads.first_name=first_name
        ads.last_name=last_name
        ads.country=country
        ads.address=address
        ads.city=city
        ads.pincode=pincode
        ads.phone=phone
        ads.email=email
        ads.state=state
        ads.order_note=order_note
        ads.save()

        return redirect('userprofile')
    

def edit_address(request,edit_id):

    if request.method == 'POST':

        first_name=request.POST.get('firstname')
        last_name=request.POST.get('lastname')
        country=request.POST.get('country')
        address=request.POST.get('address')
        city=request.POST.get('city')
        pincode=request.POST.get('pincode')
        phone=request.POST.get('phone')
        email=request.POST.get('email')
        state=request.POST.get('state')
        order_note=request.POST.get('order_note')
        
        context={
            'pre_first_name': first_name,
            'pre_last_name':last_name,
            'pre_country':country,
            'pre_address':address,
            'pre_city':city,
            'pre_ pincode':pincode,
            'pre_phone':phone,
            'pre_email':email,
            'pre_state':state,
            'pre_order_note':order_note,
    
                }


        if request.user is None:
            return
        
        if first_name.strip() == '' : 
            messages.error(request,'names cannot be empty!!!')
            context['pre_first_name']=''
            return redirect('edit_address',context)
            
        if last_name.strip() == '':
            messages.error(request,'names cannot be empty!!!')
            context['pre_last_name']=''
            return redirect('edit_address',context)
        
        if country.strip()=='':
            messages.error(request,'Country cannot be empty')
            context['pre_country']=''
            return redirect('edit_address',context)
        if city.strip()=='':
            messages.error(request,'city cannot be empty')
            context['pre_city']=''
            return redirect('edit_address',context)
        if address.strip()=='':
            messages.error(request,'address cannot be empty')
            context['pre_address']=''
            return redirect('edit_address',context)
        if pincode.strip()=='':
            messages.error(request,'pincode cannot be empty')
            context['pre_ pincode']=''
            return redirect('edit_address',context)
        if not re.search(re.compile(r'^\d{6}$'),pincode ):  
            messages.error(request,'should only 6 contain numeric!')   
            context['pre_ pincode']=''
            return redirect('edit_address',context)
        if not re.search(re.compile(r'(\+91)?(-)?\s*?(91)?\s*?(\d{3})-?\s*?(\d{3})-?\s*?(\d{4})'),phone ): 
            messages.error(request,'Enter valid phonenumber!')
            context['pre_phone']=''
            return redirect('edit_address',context)
        if phone.strip()=='':
            messages.error(request,'phone cannot be empty')
            context['pre_phone']=''
            return redirect('edit_address',context)
        if email.strip()=='':
            messages.error(request,'email cannot be empty')
            context['pre_email']=''
            return redirect('edit_address',context)
        email_check=validateemail(email)
        if email_check is False:
            messages.error(request,'email not valid!')
            context['pre_email']=''
            return redirect('edit_address',context)
                   
        if state.strip()=='':
            messages.error(request,'state cannot be empty')
            context['pre_state']=''
            return redirect('edit_address',context)

        try:
            ads = Address.objects.get(id=edit_id)
        except Address.DoesNotExist:
            messages.error(request, 'Address not found!')
            return redirect('userprofile')
        ads.user=request.user
        ads.first_name=first_name
        ads.last_name=last_name
        ads.country=country
        ads.address=address
        ads.city=city
        ads.pincode=pincode
        ads.phone=phone
        ads.email=email
        ads.state=state
        ads.order_note=order_note
        ads.save()

        return redirect('userprofile')
    else:
        return redirect('userprofile')
    
def editprofile(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')

        print(phone_number,first_name)

        if phone_number == '':
            messages.error(request, 'phone_number is empty')
            return redirect('userprofile')
        if first_name == '' or last_name == '':
            messages.error(request, 'First or Lastname is empty')
            return redirect('userprofile')
      
        try:
            user = CustomUser.objects.get(phone_number=request.user)
            print(user)
            user.phone_number = phone_number
            user.first_name = first_name
            user.last_name = last_name
            user.email=email
            user.save()
            messages.success(request, 'userprofile updated successfully')
        except:
            messages.error(request, 'User does not exist')
    return redirect('userprofile')

# Change Password 
def changepassword(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_new_password = request.POST.get('confirm_new_password')
#  Validation
        if new_password != confirm_new_password:
            messages.error(request,'Password did not match!')
            return redirect('userprofile')
        password_check=validatepassword(new_password)
        if password_check is False:
                    messages.error(request,'Enter strong password!')
                    return redirect('userprofile')
        user = CustomUser.objects.get(phone_number=request.user)
        user_password =user.password
        if old_password == user_password:
            user.set_password(new_password)
            user.save()
            AUTH_USER_MODEL.login(request,user)

            messages.success(request, 'Password updated successfully')
            return redirect('userprofile')
        else:
            messages.error(request, 'Invalid old password')
            return redirect('userprofile')
    return redirect('userprofile')

# delete Address
def deleteaddress(request,delete_id):
    address = Address.objects.get(id = delete_id)
    address.delete()
    return redirect('userprofile')

 
def validateemail(email):
    try:
        validate_email(email)
        return True
    except ValidationError: 
        return False
    
def validatepassword(new_password):
    try:
        validate_password(new_password)
        return True
    except  ValidationError:
        return  False
    
