import re
from django.shortcuts import redirect, render
from categories.models import category
from checkout.models import Order
from home.models import Contacts
from offer.models import Offer
from user.views import validateemail
from variant.models import VariantImage, Variant
from products.models import Product,Size,Color,ProductReview
from cart.models import Cart
from wishlist.models import Wishlist
from django.db.models import Q 
from django.db.models import Sum,Avg
from banner.models import banner
from datetime import datetime, timedelta
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
def home(request):
    
    if request.user.is_superuser:
        return redirect('dashboard')
    
    categories = category.objects.all()
    products = Product.objects.all()
    banners =banner.objects.all()
    reviews = ProductReview.objects.all()
    ratings = Product.objects.annotate(avg_rating=Avg('reviews__rating'))
    try:
        cart_count =Cart.objects.filter(user =request.user).count()
        wishlist_count =Wishlist.objects.filter(user=request.user).count()
    except:
        cart_count =False
        wishlist_count =False    
    # for product in ratings:    
    #     print(f"Product: {product.id}, Avg Rating: {product.avg_rating}")
        
    variant_images = (VariantImage.objects.filter(variant__product__is_available=True)
                      .order_by('variant__product').distinct('variant__product') 
                      )
    
    context={'categories': categories,
             'products': products,
             'ratings' : ratings,
             'wishlist_count':wishlist_count,
             'cart_count':cart_count,
             'reviews':reviews,
             'variant_images': variant_images,
             'banners' :banners}
    return render(request, 'home/home.html',context )

   
def product_show(request,prod_id,img_id):
  
    variant = VariantImage.objects.filter(variant=img_id,is_available=True)
    variant_images = (VariantImage.objects.filter(variant__product__id=prod_id,is_available=True)
                     .distinct('variant__product'))
    # size =VariantImage.objects.filter(variant__product__id=prod_id).distinct('variant__size')
    size =Size.objects.all()
    color=VariantImage.objects.filter(variant__product__id=prod_id,is_available=True).distinct('variant__color')
    
    reviews = ProductReview.objects.filter(product=prod_id)
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    rev_count=ProductReview.objects.filter(product=prod_id).count()
    try:
        cart_count =Cart.objects.filter(user =request.user).count()
        wishlist_count =Wishlist.objects.filter(user=request.user).count()
    except:
        cart_count =False
        wishlist_count =False 
    try:
     average_rating = int(average_rating)
    except:
        average_rating=0
    context={
        'variant':variant,
        'size':size,
        'color':color,
        'variant_images' :variant_images,    
        'reviews':reviews,
        'average_rating':average_rating ,
        'rev_count':rev_count,
        'wishlist_count':wishlist_count,
        'cart_count' :cart_count,
    }
 
    return render(request,'product/product_show.html',context)   

def user_category_show(request,category_id):
    
    variant = VariantImage.objects.filter(variant__product__category=category_id,is_available=True).distinct('variant__color')
    ratings = Product.objects.annotate(avg_rating=Avg('reviews__rating'))
    try:
        cart_count =Cart.objects.filter(user =request.user).count()
        wishlist_count =Wishlist.objects.filter(user=request.user).count()
    except:
        cart_count =False
        wishlist_count =False 
   
    context={
        'variant':variant,
        'ratings' : ratings, 
        'wishlist_count':wishlist_count,
        'cart_count' :cart_count,  
    }
    
    return render(request,'category/categoryuser.html',context)   

def search_view(request):
    
    search_query = request.POST.get('search')  
    variant_images = (VariantImage.objects.filter
                      (variant__product__product_name__icontains=search_query,is_available=True )
                      .distinct('variant__product__product_name'))
    ratings = Product.objects.annotate(avg_rating=Avg('reviews__rating'))
    try:
        cart_count =Cart.objects.filter(user =request.user).count()
        wishlist_count =Wishlist.objects.filter(user=request.user).count()
    except:
        cart_count =False
        wishlist_count =False 
    if variant_images :
       if ratings:
        pass
       else:
        ratings=False
    else:
        
        variant_images=False
    context={'variant_images': variant_images,
             'ratings': ratings,
             'wishlist_count':wishlist_count,
             'cart_count' :cart_count,  }
    return render(request, 'shop/shop.html',context )

@login_required(login_url='user_login1')    
def track_order(request):
    last_order=Order.objects.filter(user=request.user).last()
    date =last_order.created_at+timedelta(days=4)
    
    context ={
       'last_order' :last_order ,
       'date' :date
    }
    return render(request,'trackorder/trackorder.html',context)
def contact_page(request):
    
    
    return render(request,'mycontact/mycontact.html')
    

from django.core.mail import send_mail


def contact_user(request):
    if request.method == 'POST':
        
        name=request.POST['name']
        email=request.POST['email']
        phonenumber=request.POST['phonenumber']
        subject=request.POST['subject']
        message=request.POST['message']
        if (name.strip()=='' or email.strip()==''or phonenumber.strip()==''  
            or subject.strip()=='' or message.strip()=='' ):
            messages.error(request,'field cannot empty!')
            return render(request,'mycontact/mycontact.html')
        email_check=validateemail(email)
        if email_check is False:
            messages.error(request,'email not valid!')
            return render(request,'mycontact/mycontact.html')
        if not re.search(re.compile(r'(\+91)?(-)?\s*?(91)?\s*?(\d{3})-?\s*?(\d{3})-?\s*?(\d{4})'), phonenumber):   
            messages.error(request,'phonenumber should only contain numeric!')
            return render(request,'mycontact/mycontact.html')
        phonenumber_checking=len(phonenumber)
        if not  phonenumber_checking==10:
            messages.error(request,'phonenumber should be must contain 10digits!')
            return render(request,'mycontact/mycontact.html')
        contact =Contacts.objects.create(name=name,phone_number=phonenumber,email =email,subject=subject,message=message)
        contact.save()
        messages.success(request,'your contact has been submited!')
        return render(request,'mycontact/mycontact.html')
        
    

            
        

    return render(request,'mycontact/mycontact.html')
    

        