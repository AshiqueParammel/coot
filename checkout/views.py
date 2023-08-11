import random
import string
from django.shortcuts import redirect, render
from coupon.models import Coupon

from wishlist.models import Wishlist
from .models import Order, OrderItem
from products.models import Product,Size,Color
from variant.models import Variant,VariantImage
from cart.models import Cart
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from userprofile.models import Address,Wallet
from user.models import CustomUser
from django.contrib import messages

def checkout(request):
    request.session['coupon_session']=0
    if request.method == 'POST':
        coupon = request.POST.get('coupon')
        if coupon is None:
            messages.error(request, 'coupon field is cannot empty!')
            return redirect('checkout')
        try:
            check_coupons =Coupon.objects.filter(coupon_code=coupon).first()
            cartitems = Cart.objects.filter(user=request.user)
    
            total_price = 0

            for item in cartitems:
                product_price = item.variant.product.product_price
                
                total_price += product_price * item.product_qty
            grand_total = total_price
            if grand_total>=check_coupons.min_price:
                # total_price +=total_price-check_coupons.coupon_discount_amount
                coupon=check_coupons.coupon_discount_amount
                request.session['coupon_session']= coupon
                
                
                messages.success(request, 'This coupon added successfully!')
            else:
                coupon=False 
                messages.error(request, ' purchase minimum price!')    
                
            address = Address.objects.filter(user= request.user,is_available=True)
            cart_count =Cart.objects.filter(user =request.user).count()
            wishlist_count =Wishlist.objects.filter(user=request.user).count()
            coupon_checkout =Coupon.objects.filter(is_available=True)
            

            context = {
                'coupon_checkout':coupon_checkout,
                'cartitems': cartitems,
                'total_price': total_price,
                'grand_total': grand_total,
                'address': address,
                'wishlist_count':wishlist_count,
                'cart_count' :cart_count,   
                'coupon':coupon
                
            }
            if total_price==0:
                return redirect('home')
            else:
                return render(request,'checkout/checkout.html',context)
                
             
                
                
                 
        except:
            messages.error(request, 'This coupon not valid!')
            return redirect('checkout')
    
    cartitems = Cart.objects.filter(user=request.user)
    
    total_price = 0

    for item in cartitems:
        product_price = item.variant.product.product_price
        
        total_price += product_price * item.product_qty
        
    grand_total = total_price

    address = Address.objects.filter(user= request.user,is_available=True)
    cart_count =Cart.objects.filter(user =request.user).count()
    wishlist_count =Wishlist.objects.filter(user=request.user).count()
    coupon_checkout =Coupon.objects.filter(is_available=True)
    coupon =False

    context = {
        'coupon_checkout':coupon_checkout,
        'cartitems': cartitems,
        'total_price': total_price,
        'grand_total': grand_total,
        'address': address,
        'wishlist_count':wishlist_count,
        'cart_count' :cart_count,  
        'coupon':coupon
        
    }
    if total_price==0:
       return redirect('home')
    else:
           
        return render(request,'checkout/checkout.html',context)




def placeorder(request):
    if request.method == 'POST':
        # Retrieve the current user
        
        user = request.user
        # Retrieve the address ID from the form data
        coupon = request.POST.get('couponOrder')
        address_id = request.POST.get('address')
        if address_id is None:
            messages.error(request, 'Address field is mandatory!')
            return redirect('checkout')

        # Retrieve the selected address from the database
        address = Address.objects.get(id=address_id)

        # Create a new Order instance and set its attributes
        neworder = Order()
        neworder.address=address
        neworder.user = user
        neworder.payment_mode = request.POST.get('payment_method')
        neworder.message = request.POST.get('order_note')

        # Calculate the cart total price 
        cart_items = Cart.objects.filter(user=user)
        cart_total_price = 0
        
        for item in cart_items:
            product_price = item.variant.product.product_price
            cart_total_price += product_price * item.product_qty
        # print(coupon,'asdfghjkjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj')    
        
        
        coupon =int(coupon)   
        cart_total_price = cart_total_price - coupon 
        neworder.total_price = cart_total_price

        # Generate a unique tracking number
        track_no = random.randint(1111111, 9999999)
        while Order.objects.filter(tracking_no=track_no).exists():
            track_no = random.randint(1111111, 9999999)
        neworder.tracking_no = track_no

        neworder.payment_id = generate_random_payment_id(10)
        while Order.objects.filter(payment_id=neworder.payment_id).exists():
            neworder.payment_id = generate_random_payment_id(10)

        neworder.save()

        # Create OrderItem instances for each cart item
        for item in cart_items:
            OrderItem.objects.create(
                order=neworder,
                variant=item.variant,
                price=item.variant.product.product_price,
                quantity=item.product_qty
            )

            # Decrease the product quantity from the available stock
            product = Variant.objects.filter(id=item.variant.id).first()
            product.quantity -= item.product_qty
            product.save()

        # Delete the cart items after the order is placed 
            cart_items.delete()

        payment_mode = request.POST.get('payment_method')
        if payment_mode == 'cod' or payment_mode == 'razorpay' :
            
    
            return JsonResponse({'status': "Your order has been placed successfully"})
    
        
        
    return redirect('checkout')



def generate_random_payment_id(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))


def razarypaycheck(request):
    cart = Cart.objects.filter(user=request.user)
    total_price = 0
    for item in cart:
        total_price = total_price + item.variant.product.product_price * item.product_qty
    session_coupon=request.session.get('coupon_session')
    total_price = total_price - session_coupon  
    del request.session['coupon_session']  
 
         
    return JsonResponse({'total_price': total_price})

