from django.urls import path
from . import views

urlpatterns=[
    
    path('order_list/',views.order_list,name='order_list'),
    path('order_view/<int:view_id>',views.order_view,name='order_view'),
    path('change_status/',views.change_status,name='change_status'),
    path('return_order/<int:return_id>',views.return_order,name='return_order'),
    path('order_cancel/<int:cancel_id>',views.order_cancel,name='order_cancel'),
  

]