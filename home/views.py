from django.shortcuts import render
from categories.models import category
from variant.models import VariantImage, Variant
from products.models import Product,Size,Color
from cart.models import Cart
from django.db.models import Q
def home(request):
    categories = category.objects.all()
    products = Product.objects.all()
 

    # Get unique VariantImage objects based on the associated Product
    variant_images = VariantImage.objects.order_by('variant__product').distinct('variant__product')
    

    

    return render(request, 'home/home.html', {'categories': categories, 'products': products, 'variant_images': variant_images})

   
def product_show(request,prod_id,img_id):
    
    variant = VariantImage.objects.filter(variant=img_id)
    variant_images = VariantImage.objects.filter(variant__product__id=prod_id).distinct('variant__product')
    # size =VariantImage.objects.filter(variant__product__id=prod_id).distinct('variant__size')
    size =Size.objects.all()
    color=VariantImage.objects.filter(variant__product__id=prod_id).distinct('variant__color')

    context={
        'variant':variant,
        'size':size,
        'color':color,
        'variant_images' :variant_images,    
    }
    
    
    return render(request,'product/product_show.html',context)   


def user_category_show(request,category_id):
    
    variant = VariantImage.objects.filter(variant__product__category=category_id).distinct('variant__color')
   

    context={
        'variant':variant,   
    }
    
    
    return render(request,'category/categoryuser.html',context)   


# 

def search_view(request):
    
    search_query = request.POST.get('search')  
    

    variant_images = VariantImage.objects.filter(variant__product__product_name__icontains=search_query ).distinct('variant__product__product_name')

    if variant_images :
       pass
    else:
     
        variant_images=False

    return render(request, 'shop/shop.html', {'variant_images': variant_images})

    
    