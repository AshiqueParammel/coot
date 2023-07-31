from django.urls import path
from . import views

urlpatterns=[
    
    path('order_list/',views.order_list,name='order_list'),
    path('order_view/<int:view_id>',views.order_view,name='order_view'),
    path('change_status/',views.change_status,name='change_status'),
      
]