from django.shortcuts import render
from products.models import Product,Size,Color
from variant.models import Variant,VariantImage
# Create your views here.
def cart(request,prod_id):
    
    variant_ = VariantImage.objects.filter(variant__product__id=prod_id)
    variant_images = VariantImage.objects.filter(variant__product__id=prod_id).distinct('variant__product')
    size =VariantImage.objects.filter(variant__product__id=prod_id).distinct('variant__size')
    color=VariantImage.objects.filter(variant__product__id=prod_id).distinct('variant__color')
        
    context={
        'variant':variant_images,
        'size':size,
        'color':color,
        'var':variant_,
        
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
    

