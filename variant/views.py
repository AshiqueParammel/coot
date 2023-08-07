from django.shortcuts import render,redirect
import webcolors
from django.db.models import Sum,Count
from .models import Product,Size,Color,Variant,VariantImage
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.core.exceptions import ObjectDoesNotExist
from .forms import ImageForm
from django.http import JsonResponse
# Create your views here.
    
def product_variant(request):
    if not request.user.is_superuser:
        return redirect('admin_login1')
    variant = Variant.objects.all().order_by('id') 
    size_range= Size.objects.all().order_by('id')
    color_name= Color.objects.all().order_by('id')
    product=Product.objects.all().order_by('id')
    variant_list={
        'variant'    :variant,
        'size_range' :size_range,
        'color_name' :color_name, 
         'product'   :product,
    }
    return render(request,'variant/variant.html',{'variant_list':variant_list})  

def add_Product_Variant(request):
    if not request.user.is_superuser:
        return redirect('admin_login1')

    if request.method == 'POST':
        variant_name = request.POST.get('variant_name')
        variant_size = request.POST.get('variant_size')
        variant_color = request.POST.get('variant_color')
        variant_quantity = request.POST.get('variant_quantity')

        # Validation
        if variant_quantity.strip() == '':
            messages.error(request, "Quantity field is empty!")
            return redirect('product_variant')

        try:
            product_obj = Product.objects.get(id=variant_name)
            size_obj = Size.objects.get(id=variant_size)
            color_obj = Color.objects.get(id=variant_color)

            # Check if variant already exists
            if Variant.objects.filter(product=product_obj, size=size_obj, color=color_obj).exists():
                messages.error(request, "Variant with the same product, size, and color already exists!")
                return redirect('product_variant')

            # Save new variant
            add_variant = Variant(
                product=product_obj,
                color=color_obj,
                size=size_obj,
                quantity=variant_quantity,
            )
            add_variant.save()

            messages.success(request, 'Variant added successfully!')
            return redirect('product_variant')

        except ObjectDoesNotExist:
            messages.error(request, "Invalid product, size, or color selected!")
            return redirect('product_variant')

    return render(request, 'variant/variant.html')

def edit_prodectvariant(request,variant_id):
    if not request.user.is_superuser:
        return redirect('admin_login1')
    
    if request.method == 'POST':
        variant_name = request.POST.get('variant_name')
        variant_size = request.POST.get('variant_size')
        variant_color = request.POST.get('variant_color')
        variant_quantity = request.POST.get('variant_quantity')
        
        if variant_quantity.strip() == '':
            messages.error(request, "Quantity field is empty!")
            return redirect('product_variant')
        
     
        product_obj = Product.objects.get(id=variant_name)
        size_obj = Size.objects.get(id=variant_size)
        color_obj = Color.objects.get(id=variant_color)

        # Check if variant already exists
        if Variant.objects.filter(product=product_obj, size=size_obj, color=color_obj).exists():
            check = Variant.objects.get(id=variant_id)
            if product_obj==check.product and size_obj==check.size and color_obj==check.color:
                pass
            else:
                messages.error(request, "Variant with the same product, size, and color already exists!")
                return redirect('product_variant')
        
        edit_variant=Variant.objects.get(id=variant_id)
        edit_variant.color=color_obj
        edit_variant.size=size_obj
        edit_variant.product=product_obj
        edit_variant.quantity=variant_quantity
        edit_variant.save()
        messages.success(request,'product edited successfully!')
        
        return redirect('product_variant') 
            
def prodectvariant_delete(request, variant_id):  
    if not request.user.is_superuser:
        return redirect('admin_login1')
    delete_productvariant = Variant.objects.get(id=variant_id) 
    delete_productvariant.delete()
    messages.success(request,'product_variant deleted successfully!')
    return redirect('product_variant')       
    
def product_size(request):
    if not request.user.is_superuser:
            return redirect('admin_login1')   
    products_size=Size.objects.all().order_by('id')
    return render(request,'size_management/size_management.html',{'products_size':products_size})

def add_size(request):
    if not request.user.is_superuser:
        return redirect('admin_login1')

    if request.method == 'POST':
        size = request.POST.get('size')  
        if  size.strip() == '':
            messages.error(request, 'Field cannot be empty!')
            return redirect('product_size')

        if Size.objects.filter(size_range=size).exists():
            messages.error(request, 'Size already exists')
            return redirect('product_size')

        size_object = Size(size_range=size)
        size_object.save()
        messages.success(request,'Size added successfully!')
        return redirect('product_size')

    return render(request, 'size_management/size_management.html')

def size_delete(request, size_range_id):  
    if not request.user.is_superuser:
        return redirect('admin_login1')
    delete_size = Size.objects.get(id=size_range_id) 
    delete_size.delete()
    messages.success(request,'Size deleted successfully!')
    return redirect('product_size') 

def product_color(request):
    if not request.user.is_superuser:
            return redirect('admin_login1')   
    products_color=Color.objects.all().order_by('id')
    return render(request,'color_management/color_management.html',{'products_color':products_color})

def add_color(request):
    if not request.user.is_superuser:
        return redirect('admin_login1')

    if request.method == 'POST':
        colorname = request.POST.get('color1')  
        color = request.POST.get('color')  
        color1=color
        
        color= get_color_name(color)
        if color == "Unknown":
            color=color1
        
        if colorname.strip() == '':
            messages.error(request, 'Field cannot be empty!')
            return redirect('product_color')

        if Color.objects.filter(color_name=colorname).exists():
            messages.error(request, 'color already exists!')
            return redirect('product_color')

        color_object = Color(color_name=colorname,color_code=color)
        color_object.save()
        
        messages.success(request,'color add successfully!')

        return redirect('product_color')

    return render(request, 'color_management/color_management.html')

def color_delete(request, color_name_id):  
    if not request.user.is_superuser:
        return redirect('admin_login1')
    delete_color =Color.objects.get(id=color_name_id) 
    delete_color.delete()
    messages.success(request,'color deleted successfully!')
    return redirect('product_color') 
   
def get_color_name(color_code):
    try:
        color_name = webcolors.rgb_to_name(webcolors.hex_to_rgb(color_code))
        return color_name
    except ValueError:
        return "Unknown"
    
    
def image_list(request,variant_id):
    if not request.user.is_superuser:
        return redirect('admin_login1')
  
    image=VariantImage.objects.filter(variant=variant_id)
    add_image =variant_id
    return render(request,'variant/image_management.html',{'image':image,'add_image':add_image})
    
#  This is image add function         
def image_view(request, img_id):
    
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        var = Variant.objects.get(id=img_id)

        if form.is_valid():
            image_instance = form.save(commit=False)  
            image_instance.variant = var  
            image_instance.save()  

            print("Image saved successfully!")
            
            return JsonResponse({'message': 'works','img_id':img_id})
        else:
            print("Form is not valid:", form.errors)
            
    else:
        form = ImageForm()

    context = {'form': form,'img_id':img_id}
    return render(request, 'variant/image_add.html', context)

def image_delete(request, image_id):  
    if not request.user.is_superuser:
        return redirect('admin_login1')
    try:
        delete_image =VariantImage.objects.get(id=image_id)
        var_id= delete_image.variant.id 
        delete_image.delete()
        messages.success(request,'image deleted successfully!')
        image=VariantImage.objects.filter(variant=var_id)
        add_image =var_id
        return render(request,'variant/image_management.html',{'image':image,'add_image':add_image})
    except:
           return redirect('product_variant') 
       
       
       
def product_variant_view(request,product_id):
    if not request.user.is_superuser:
        return redirect('admin_login1')
  
    variant=VariantImage.objects.filter(variant__product=product_id)
    size_range= Size.objects.all().order_by('id')
    color_name= Color.objects.all().order_by('id')
    product=Product.objects.all().order_by('id')
    variant_list={
        'variant'    :variant,
        'size_range' :size_range,
        'color_name' :color_name, 
         'product'   :product,
    }
    # variant_id
    return render(request,'view/variant_view.html',{'variant_list':variant_list})       
       
       

    
       
            


    
 