from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,redirect
from checkout.models import Order,OrderItem
from userprofile.models import Address
from variant.models import Variant,VariantImage
from cart.models import Cart
from django.contrib import messages
# Create your views here.


def order_list(request):
    
    order =Order.objects.all()
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
        image = VariantImage.objects.filter(variant__id__in=variant_ids).distinct('variant__product')
        context = {
            'orderview': orderview,
            'address': address,
            'products': products,
            'image' :image,
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
    orderitems = OrderItem.objects.get(id = orderitem_id)
    
    print(orderitem_id,'11111111111111111111111111111111')
 
   

    orderitems.status = order_status
    orderitems.order.od_status = order_status
    print(orderitems.order.od_status,'111111111111111111111111111115647')
    orderitems.save()
    view_id= orderitems.order.id
    change_status=Order.objects.get(id=view_id)
    change_status.od_status=order_status
    change_status.save()
    
    messages.success(request,'status updated!')
    return redirect('order_view',view_id)


def change_status_order(request):
    
    if not request.user.is_superuser:
        return redirect('admin_login1')
    orderitem_id = request.POST.get('orderitem_id')
    order_status = request.POST.get('status')
    change_status=Order.objects.get(id=orderitem_id)
    change_status.od_status = order_status
    change_status.save()
    
    messages.success(request,'Order status updated!')
    return redirect('order_list')

