from django.shortcuts import render,redirect
from django.http import HttpResponse

import products
from .models import Product
from categories.models import category

from django.db.models import Sum
from django.db.models.functions import TruncDay
from django.db.models import DateField
from django.db.models.functions import Cast
from datetime import datetime,timedelta
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError



@login_required(login_url='admin_login1')
def product(request):
    if not request.user.is_superuser:
        return redirect('admin_login1')
    product = Product.objects.all().order_by('id')   
    product_list={
        'product' : product,
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

        