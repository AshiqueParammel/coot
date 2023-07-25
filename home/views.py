from django.shortcuts import render
from categories.models import category
from variant.models import VariantImage, Variant
from products.models import Product
from cart.models import Cart

def home(request):
    categories = category.objects.all()
    products = Product.objects.all()

    # Get unique VariantImage objects based on the associated Product
    variant_images = VariantImage.objects.order_by('variant__product').distinct('variant__product')

    return render(request, 'home/home.html', {'categories': categories, 'products': products, 'variant_images': variant_images})

   


def product_show(request,prod_id,img_id):
    
    variant = VariantImage.objects.filter(variant=img_id)
    variant_images = VariantImage.objects.filter(variant__product__id=prod_id).distinct('variant__product')
    size =VariantImage.objects.filter(variant__product__id=prod_id).distinct('variant__size')
    color=VariantImage.objects.filter(variant__product__id=prod_id).distinct('variant__color')
    cart = Cart.objects.filter(user=request.user, variant=prod_id)
        
    context={
        'variant':variant,
        'size':size,
        'color':color,
        'variant_images' :variant_images,    
        'cart':cart
    }
    
    
    return render(request,'product/product_show.html',context)   
