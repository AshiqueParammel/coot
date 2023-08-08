from django.db.models import Sum,Avg
from django.shortcuts import render
from categories.models import category
from variant.models import VariantImage, Variant
from products.models import Product,Size,Color
from cart.models import Cart
from wishlist.models import Wishlist

def Shop(request):
    

    # Get unique VariantImage objects based on the associated Product
    variant_images = VariantImage.objects.filter(variant__product__is_available=True).order_by('variant__product').distinct('variant__product')

    ratings = Product.objects.annotate(avg_rating=Avg('reviews__rating'))
    try:
        cart_count =Cart.objects.filter(user =request.user).count()
        wishlist_count =Wishlist.objects.filter(user=request.user).count()
    except:
        cart_count =False
        wishlist_count =False 
    

    return render(request, 'shop/shop.html', {  'variant_images': variant_images,'ratings':ratings,'wishlist_count':wishlist_count,'cart_count' :cart_count,})

# def Quick_view(request,img_id):
#     try:
#          variant= Variant.objects.get(id=img_id)
#          image =VariantImage.objects.get(variant=img_id)
#          return render(request, 'shop/quick_view.html', {  'image': image,'variant':variant})
#     except:
        
#         return render(request, 'shop/shop.html')
             
         
    
