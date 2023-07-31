from django.shortcuts import render
from categories.models import category
from variant.models import VariantImage, Variant
from products.models import Product,Size,Color
from cart.models import Cart

def Shop(request):
    

    # Get unique VariantImage objects based on the associated Product
    variant_images = VariantImage.objects.order_by('variant__product').distinct('variant__product')

    return render(request, 'shop/shop.html', {  'variant_images': variant_images})

# def Quick_view(request,img_id):
#     try:
#          variant= Variant.objects.get(id=img_id)
#          image =VariantImage.objects.get(variant=img_id)
#          return render(request, 'shop/quick_view.html', {  'image': image,'variant':variant})
#     except:
        
#         return render(request, 'shop/shop.html')
             
         
    
