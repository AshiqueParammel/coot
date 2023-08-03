from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,redirect
from checkout.models import Order,OrderItem,Orderstatus,Itemstatus
from userprofile.models import Address
from variant.models import Variant,VariantImage
from cart.models import Cart
from django.contrib import messages
# Create your views here.


def order_list(request):
    
    order =Order.objects.all().order_by('id')
    
    context={
        'order':order,
    }
    
    return render(request,'adminside/order.html',context)


def order_view(request, view_id):
    
    try:
        orderview = Order.objects.get(id=view_id)
        address = Address.objects.get(id=orderview.address.id)
        products = OrderItem.objects.filter(order=view_id)
        variant_ids = [product.variant.id for product in products]
        image = VariantImage.objects.filter(variant__id__in=variant_ids).distinct('variant__color')
        item_status_o=Itemstatus.objects.all()
        context = {
            'orderview': orderview,
            'address': address,
            'products': products,
            'image' :image,
            'item_status_o' : item_status_o 
        }
        
            
            
            
        return render(request, 'View/order_view.html', context)
    except Order.DoesNotExist:
        print("Order does not exist")
    except Address.DoesNotExist:
        print("Address does not exist")
    return redirect('order_list')

def change_status(request):
    
    if not request.user.is_superuser:
        return redirect('admin_login1')
    orderitem_id = request.POST.get('orderitem_id')
    order_status = request.POST.get('status')
    order_variant = request.POST.get('variant_id')
    
    orderitems = OrderItem.objects.get(variant=order_variant, id=orderitem_id)
    item_status_instance = Itemstatus.objects.get(id=order_status)

    orderitems.orderitem_status = item_status_instance
    orderitems.save()
    view_id= orderitems.order.id
    
   
    # total item_status
    all_order_item =OrderItem.objects.filter(order=view_id)
    Pending =0
    Processing=0
    Shipped=0
    Delivered =0
    Cancelled=0
    Return=0
    
    for i in all_order_item:
        # pending
        if i.orderitem_status.id == 1 :
            Pending = Pending+1
           # Processing    
        if i.orderitem_status.id == 2 :
            Processing = Processing+1 
         # Shipped    
        if i.orderitem_status.id == 3 :
            Shipped = Shipped+1
         # deliverd    
        if i.orderitem_status.id == 4 :
            Delivered = Delivered+1           
        # Cancelled    
        if i.orderitem_status.id == 5 :
            Cancelled = Cancelled+1
         # Return    
        if i.orderitem_status.id == 6 :
            Return = Return+1    
            
    total_item =len(all_order_item)
    total_value =1  
    if total_item == Pending: 
       total_value = 1   
    elif total_item == Processing: 
       total_value = 2      
    elif total_item == Shipped: 
       total_value = 3      
    elif total_item == Delivered: 
       total_value = 4     
    elif total_item == Cancelled: 
       total_value = 5    
    elif total_item == Return: 
        total_value = 6
         
    change_all_items_status = Order.objects.get(id = view_id)
    item_status_instance_all = Orderstatus.objects.get(id=total_value)
    change_all_items_status.order_status = item_status_instance_all
    change_all_items_status.save()
    
    messages.success(request,'status updated!')
    return redirect('order_view',view_id)


# def change_status_order(request):
    
#     if not request.user.is_superuser:
#         return redirect('admin_login1')
#     orderitem_id = request.POST.get('orderitem_id')
#     order_status = request.POST.get('status')
#     change_status=Order.objects.get(id=orderitem_id)
#     change_status.od_status = order_status
#     change_status.save()
    
#     messages.success(request,'Order status updated!')
#     return redirect('order_list')

