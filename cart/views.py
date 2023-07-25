from django.shortcuts import redirect, render
from products.models import Product,Size,Color
from variant.models import Variant,VariantImage
# from user.models import CustomUser
from django.http import JsonResponse
from .models import Cart
# Create your views here.
def cart(request):
    
    
        cart = Cart.objects.filter(user=request.user).order_by('id')
        variants = cart.values_list('variant', flat=True)
        img = VariantImage.objects.filter(variant__in=variants).distinct('variant')
    
        total_price = 0
        tax = 0
        grand_total =0
        single_product_total = [0]
        for item in cart:
        
            total_price = total_price + item.variant.product.product_price * item.product_qty
            single_product_total.append(item.variant.product.product_price * item.product_qty)
            tax = total_price * 0.18
            grand_total = total_price + tax

        context = {
            'cart' : cart,
            'total_price' : total_price,
            'tax' : tax,
            'grand_total' : grand_total,
            'single_product_total':single_product_total,
            'img':img,
        }
        
        return render(request,'cart/cart.html',context)

def remove_cart(request,prod_id):
    var =prod_id
    remove =1
    context={
        'var':var,
        remove:True,
    }
    
    
    return render(request,'cart/cart.html',context)


def add_cart(request):
    if request.method =='POST':
        if request.user.is_authenticated:
            
            variant_id = request.POST.get('variant_id')
            add_qty =int(request.POST.get('add_qty'))
            try:
                variant_check =Variant.objects.get(id=variant_id)
                
            except Variant.DoesNotExist:
                return JsonResponse({'status': 'No such prodcut found'})
              
            if Cart.objects.filter(user=request.user, variant_id=variant_id).exists():
                
                return JsonResponse({'status': 'Product already in cart'})
            
        
            else:
                variant_qty = add_qty
                
                if variant_check.quantity >= variant_qty:
                    Cart.objects.create(user=request.user, variant_id=variant_id, product_qty=variant_qty)
    
                    return JsonResponse({'status': 'Product added successfully'})
                else:
                    return JsonResponse({'status': "Only few quantity available"})
        else:
            return JsonResponse({'status': 'Login to continue'})
    return redirect('product_detail')    

                 
    
    

