from django.shortcuts import render,redirect
from variant.models import Variant,VariantImage
from products.models import Size,Color,Product
from .models import Product
from categories.models import category
from variant.models import Variant
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required



@login_required(login_url='admin_login1')
def product(request):
    if not request.user.is_superuser:
        return redirect('admin_login1')
    product = Product.objects.all().order_by('id') 
   
    
    
    product_list={
        'product' : product,
        # 'variant'  : variant,
        'categories' : category.objects.all(),
 
       
    }
    return render(request,'product/products.html',product_list)

@login_required(login_url='admin_login1')
def addproduct(request):
    if not request.user.is_superuser:
        return redirect('admin_login1')
    if request.method == 'POST':
        name = request.POST['product_name']
        price = request.POST['product_price']
        category_id = request.POST.get('category')
        product_description = request.POST.get('product_description')
        # Validation
        if Product.objects.filter(product_name=name).exists():
            messages.error(request, 'Product name already exists')
            return redirect('product')
      
        if name.strip() == '' or price.strip() == '':
            messages.error(request, "Name or Price field are empty!")
            return redirect('product')
       
        category_obj = category.objects.get(id=category_id)
        
       
        # Save        
        product = Product(
          
            product_name=name,
            category=category_obj,
            product_price=price,
            slug=name,
            product_description=product_description,

        )
        product.save()
        messages.success(request,'product added successfully!')
        return redirect('product')
    
    return render(request, 'products/products.html')


def product_delete(request, product_id):  
    if not request.user.is_superuser:
        return redirect('admin_login1')
    delete_product = Product.objects.get(id=product_id) 
    delete_product.delete()
    messages.success(request,'product deleted successfully!')
    return redirect('product') 

def product_edit(request,product_id):
    if not request.user.is_superuser:
        return redirect('admin_login1')
    if request.method == 'POST':
        name = request.POST['product_name']
        price = request.POST['product_price']
        category_id = request.POST.get('category')
        product_description = request.POST.get('product_description')
         
        if name.strip() == '' or price.strip() == '':
                messages.error(request, "Name or Price field are empty!")
                return redirect('product')
        
        category_obj = category.objects.get(id=category_id)    
        
        if Product.objects.filter(product_name=name).exists():
            
            check = Product.objects.get(id=product_id)
            
            if name == check.product_name:
                pass
            else:
                messages.error(request, 'Product name already exists')
                return redirect('product')
                    
        editproduct= Product.objects.get(id=product_id)
        editproduct.product_name= name
        editproduct.product_price=price
        editproduct.category=category_obj
        editproduct.product_description=product_description
        editproduct.save()
        messages.success(request,'product edited successfully!')
        
        return redirect('product') 

    
def product_view(request,product_id):
    if not request.user.is_superuser:
        return redirect('admin_login1')
  
    variant=Variant.objects.filter(product=product_id)
    size_range= Size.objects.all().order_by('id')
    color_name= Color.objects.all().order_by('id')
    product=Product.objects.all().order_by('id')
    variant_list={
        'variant'    :variant,
        'size_range' :size_range,
        'color_name' :color_name, 
         'product'   :product,
    }
    return render(request,'View/product_view.html',{'variant_list':variant_list})  


  