from django.shortcuts import render
from categories.models import category
from variant.models import VariantImage, Variant
from products.models import Product,Size,Color,ProductReview
from cart.models import Cart
from django.db.models import Q 
from django.db.models import Sum,Avg
from banner.models import banner
def home(request):
    categories = category.objects.all()
    products = Product.objects.all()
    banners =banner.objects.all()
    count=0
    rating=0
    reviews = ProductReview.objects.all()
    
    
    
    for review in reviews:
        
        if review.product.id == 3:
            count+=1
            rating+=review.rating
            print(count,rating,'checkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk')
            
    if count ==0 and rating==0:
        avga=0
        print(avga,'cheeeeeeeeeeeeeeeeeeeeeeeeeeeeee')
    else:       
        avga=rating//count
        print(avga,'cheeeeeeeeeeeeeeeeeeeeeeeeeeeeee')
    # annotate

    
 
        
            
        
    
        
              
     
                                         
   
    # average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    # rev_count=ProductReview.objects.filter(product_id=product.id).count()
    

    # Get unique VariantImage objects based on the associated Product
    variant_images = VariantImage.objects.order_by('variant__product').distinct('variant__product')
    # 'average_rating':average_rating ,'rev_count':rev_count,
     
        
        
    

    return render(request, 'home/home.html', {'categories': categories, 'products': products,'reviews':reviews, 'variant_images': variant_images,'banners' :banners})

   
def product_show(request,prod_id,img_id):
  
    
    variant = VariantImage.objects.filter(variant=img_id)
    variant_images = VariantImage.objects.filter(variant__product__id=prod_id).distinct('variant__product')
    # size =VariantImage.objects.filter(variant__product__id=prod_id).distinct('variant__size')
    size =Size.objects.all()
    color=VariantImage.objects.filter(variant__product__id=prod_id).distinct('variant__color')
    
    reviews = ProductReview.objects.filter(product=prod_id)
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg']

    rev_count=ProductReview.objects.filter(product=prod_id).count()
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

    
    