from django.shortcuts import redirect, render
from variant.models import Variant,VariantImage
from django.http import JsonResponse

from wishlist.models import Wishlist
from .models import Cart
from django.contrib.auth.decorators import login_required
from django.contrib import messages,auth
# Create your views here.
@login_required(login_url='user_login1')
def cart(request):
    
    
    if request.user.is_authenticated:
    
        cart = Cart.objects.filter(user=request.user).order_by('id')
        variants = cart.values_list('variant', flat=True)
        img = VariantImage.objects.filter(variant__in=variants).distinct('variant')
        cart_count =Cart.objects.filter(user =request.user).count()
        wishlist_count =Wishlist.objects.filter(user=request.user).count()
    
        total_price = 0
        tax = 0
        grand_total =0
        single_product_total = 0
        for item in cart:
        
            total_price = total_price + item.variant.product.product_price * item.product_qty
            single_product_total+item.variant.product.product_price * item.product_qty
            tax = total_price * 0.18
            grand_total = total_price + tax
            

        context = {
            'cart' : cart,
            'total_price' : total_price,
            'tax' : tax,
            'grand_total' : grand_total,
            'single_product_total':single_product_total,
            'img':img,
            'wishlist_count':wishlist_count, 
            'cart_count':cart_count,
        }
        
        return render(request,'cart/cart.html',context)
    else:
        return render(request,'cart/cart.html')
        
@login_required(login_url='user_login1')
def remove_cart(request,cart_id):
    try:
        cart_remove = Cart.objects.get(id=cart_id)
        
        cart_remove.delete()
        messages.success(request,'product removed from cart successfully!')
    except:
        return redirect('cart')
               
    return redirect('cart')

# @login_required(login_url='user_login1')
def add_cart(request):
    if request.method =='POST':
        if request.user.is_authenticated:
            
            variant_id = request.POST.get('variant_id')
            add_qty =int(request.POST.get('add_qty'))
            add_size =request.POST.get('add_size')
            try:
                variant_check =Variant.objects.get(id=variant_id )
                if variant_check.size==add_size:
                    pass
                else:
                    product=variant_check.product
                    color= variant_check.color
                    try:
                        check_variant=Variant.objects.get(product=product, color=color, size=add_size)
                        variant_id= check_variant.id
                    except Variant.DoesNotExist:
                        return JsonResponse({'status': 'Sorry! this variant not available'})  
                        
            except Variant.DoesNotExist:
                return JsonResponse({'status': 'No such prodcut found'})
              
            if Cart.objects.filter(user=request.user, variant_id=variant_id).exists():
                
                return JsonResponse({'status': 'Product already in cart'})
            
        
            else:
                variant_qty = add_qty
                
                if variant_check.quantity >= variant_qty:
                    total = variant_qty*variant_check.product.product_price
                    Cart.objects.create(user=request.user, variant_id=variant_id, product_qty=variant_qty,single_total=total)
    
                    return JsonResponse({'status': 'Product added successfully'})
                else:
                    return JsonResponse({'status': "Only few quantity available"})
        else:
            return JsonResponse({'status': 'you are not login please Login to continue'})
            
            
    return redirect('home')    

                 
    
@login_required(login_url='user_login1')
def update_cart(request):
    if request.method == 'POST':
        cart_id = request.POST.get('cart_id')
        if (Cart.objects.filter(user=request.user, id=cart_id)):
            prod_qty =int (request.POST.get('product_qty'))
           
            cart = Cart.objects.get(id=cart_id, user=request.user)
            cartes = cart.variant.quantity
            if int(cartes) >= int(prod_qty):
                cart.product_qty = prod_qty
                single=cart.single_total =prod_qty*cart.variant.product.product_price
           
                
                cart.save()

                carts = Cart.objects.filter(user = request.user).order_by('id')
                total_price = 0
                for item in carts:
                    total_price = total_price + item.variant.product.product_price * item.product_qty
                
                    
                return JsonResponse({'status': 'Updated successfully','sub_total':total_price,'single':single, 'product_price':cart.variant.product.product_price,'quantity':prod_qty})
            else:
                return JsonResponse({'status': 'Not allowed this Quantity'})
    return JsonResponse('something went wrong, reload page',safe=False)