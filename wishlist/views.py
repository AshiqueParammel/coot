from django.shortcuts import redirect, render
from cart.models import Cart
from variant.models import Variant,VariantImage
from django.http import JsonResponse
from .models import Wishlist
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Size

# Create your views here.
@login_required(login_url='user_login1')
def wish_list(request):
    if request.user.is_authenticated:
        wishlist = Wishlist.objects.filter(user=request.user).order_by('id')
        variants = wishlist.values_list('variant', flat=True)
        img = VariantImage.objects.filter(variant__in=variants).distinct('variant')
        cart_count =Cart.objects.filter(user =request.user).count()
        wishlist_count =Wishlist.objects.filter(user=request.user).count()
        size =Size.objects.all()
       
        
        context = {
                'wishlist' : wishlist,
                'img':img,
                'size':size,
                'cart_count':cart_count,
                'wishlist_count' : wishlist_count,  
            }
        return render(request,'wishlist/wishlist.html',context)
    else:
        return render(request,'wishlist/wishlist.html')



# @login_required(login_url='user_login1')
def add_wish_list(request):
    if request.method =='POST':
        if request.user.is_authenticated:
            
            variant_id = request.POST.get('variant_id')
            add_size =request.POST.get('add_size')
            # try:
            #     variant_check =Variant.objects.get(id=variant_id )
            #     if variant_check.size==add_size:
            #         pass
            #     else:
            #         product=variant_check.product
            #         color= variant_check.color
            #         try:
            #             check_variant=Variant.objects.get(product=product, color=color, size=add_size)
            #             variant_id= check_variant.id
            #         except Variant.DoesNotExist:
            #             return JsonResponse({'status': 'Sorry! this variant not available'})  
                        
            # except Variant.DoesNotExist:
            #     return JsonResponse({'status': 'No such prodcut found'})
              
            if Wishlist.objects.filter(user=request.user, variant_id=variant_id).exists():
                
                return JsonResponse({'status': 'Product already in Wishlist'})
            
        
            else:
                Wishlist.objects.create(user=request.user, variant_id=variant_id)
                return JsonResponse({'status': 'Product added successfully in Wishlist'})    
        else:
            return JsonResponse({'status': 'you are not login please Login to continue'})
            
            
    return redirect('home')    


       
@login_required(login_url='user_login1')
def remove_wish_list(request,wish_id):
    
    try:
        Wishlist_remove = Wishlist.objects.get(id=wish_id)
        
        Wishlist_remove.delete()
        messages.success(request,'product removed from wishlist successfully!')
    except:
        return redirect('wish_list')
               
    return redirect('wish_list')    